from argparse import Namespace
import os
from pathlib import Path
import re

from typing import Any, Callable, List, Literal, Optional, Tuple, TYPE_CHECKING

from mkdocs.config import config_options  as C
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_addresses import path_manager

from .exceptions import AddresserConfigError, InvalidOperationError

if TYPE_CHECKING:
    from .addresses_plugin import AddressAddressesPlugin






# Definition used for mkdocstrings
class PluginOptions(Namespace):


    activate_cache: bool = True
    """
    Exploring and cross-checking all references in the documents can be rather time consuming
    because of the way it is done in the plugin (exploring the resulting html content) which
    means the plugin could significantly slow down the serve operations when the number of
    documents or their size becomes rather big.

    To limit this problem, the plugin uses a cache (activated by default).

    If activated, only the recently modified markdown files will be explored again on next
    serve. This allows to drastically reduce the serving time, while the plugin still can
    check for outdated references in the unchanged pages, since their content is cached.

    Note that when mkdocs starts, all pages must be explored at least once, so the first serve
    operation can be very slow on big documentations.
    """


    dump_action: str = 'normal'
    """
    The plugin normally dumps information about all the available references (see
    [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
    option) on each serve.

    The `dump_action` determines what the plugin does about the
    [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file].

    * `normal`: the plugin recreates the informations on each serve.
    * `none`: the plugin uses its normal behavior, but the
      [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
      is not updated.
    * `only`: the plugin will skip all the addresses verifications in the documentation files and
      will only gather the references definitions, drop all of them in the
      [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file],
      then raise `DumpOnlyError` to stop serving.

        This option may come in handy if you need to regenerate the code snippets while something
        normally causes a crash during the addresses verifications.
    """


    dump_file_vsc: str = '.vscode/links.code-snippets'
    dump_file_txt: str = 'addresses_identifiers.txt'
    dump_snippets_file: str = ''
    """
    Define the location of the file where the information about all the references will be
    saved (relative to the cwd).

    There are a number of restrictions on the possible values of this option:

    * The targeted file cannot be in the `docs_dir` (it should never be anyway).
    * The extension of the file must be compatible with the value chosen for the
    [`use_vsc`][mkdocs_addresses.config_plugin.PluginOptions.use_vsc]
    option.
    * If left undefined, the filename is chosen depending on the
    [`use_vsc`][mkdocs_addresses.config_plugin.PluginOptions.use_vsc] option.

    | `use_vsc` | Default `dump_snippets_file` | File extension |
    |:-|:-|:-|
    | `true` | `.vscode/links.code-snippets` | `.code-snippets` |
    | `false` | `addresses_identifiers.txt` | `.txt` |
    """


    external_links_file: str = ''
    """
    Location of the file, if any, where are defined the global links, like:

    ```markdown
    [mkdocs]: https://www.mkdocs.org/ "mkdocs - home"
    [id]: address "tooltip"
    ...
    ```

    If this option is defined:

    - This file cannot be in the docs_dir itself (it shouldn't anyway).
    - All links defined in this file must be absolute or the plugin will raise an error. This
      restriction can be bypassed by "white listing" the address (see
      [`links_white_list`][mkdocs_addresses.config_plugin.PluginOptions.links_white_list] and
      [`links_white_list_pattern`][mkdocs_addresses.config_plugin.PluginOptions.links_white_list_pattern]).
    - This file should be appended automatically to all files through the `pymdownx.snippets`
      markdown extension, directly in the `mkdocs.yml` file. For example:

        ```yaml
        markdown_extensions:
            - pymdownx.snippets:
                check_paths: true
                auto_append: ["docs_logistic/external-links.md"]

        plugins:
            - mkdocs-addresses:
                extenral_links_file: docs_logistic/external-links.md
        ```
    """


    fail_fast: bool = False
    """
    Defines if the errors raised by the plugin will interrupt the serve operations or will only
    result in feedback in the console.

    When writing the docs, it may be useful to pass this option to false: this way, there is no
    need to restart the serving each time a link is wrong and you can keep working, fixing the
    errors step by step.

    Note that if `fail_fast` is false, a summary of all the wrong addresses found will be
    displayed once all the pages have been checked. This is especially useful if there are
    a lot of errors and the console becomes somewhat cluttered with messages.
    """


    imgs_extension_pattern: str = "\\.(jpg|jpeg|bmp|png|svg)$"
    """
    Regex string used to identify picture files (using
    [`re.search`](https://docs.python.org/3/library/re.html#re.search){: target=_blank }).
    """


    ignore_auto_headers: bool = True
    """
    By default, mkdocs turns the content of each header into an html id that can be used as anchor.

    Considering how the plugin builds the references, and that it forbids duplicate identifiers,
    this would mean that duplicated titles would be impossible to use across the same project
    documentation. Which would be... rather unfortunate.

    There are several ways to circumvent this:

    1. Define an id attribute for the problematic headers: `## duplicate title {: #unique-id }`
      (reminder: this supposes you are using the `attr_list` markdown extension).
    1. Add the automatically generated id to the list of [`ignored_ids`][mkdocs_addresses.config_plugin.PluginOptions.ignored_ids].
    1. "White list" the id, [one way][mkdocs_addresses.config_plugin.PluginOptions.links_white_list]
      or [another][mkdocs_addresses.config_plugin.PluginOptions.links_white_list_pattern].
    1. Set `ignore_auto_headers` to true. The plugin will then attempt to spot the automatic
    identifiers and ignore them.

        Note that false negative can occur from time to time: when the plugin is searching for
        references in the html code, it tries to compare the content of the headers with the
        html id and ignores it if it is considered equivalent to the content (roughly: it
        converts the text content to a "simplified kebab-case", removing some special characters,
        then compares the result to the id).

    For example:

    * With `ignore_auto_headers` set to false:

    ```markdown
    ## Content
    ...

    ### Content

    This second title raises DuplicateIdentifierError (even with a different header level)

    ## Content {: #precedence }
    This title wouldn't cause problems, because its id will be used instead
    ```

    * With `ignore_auto_headers` set to true:

    ```markdown
    ## Content
    ... is ignored

    ## Content
    ... is also ignored

    ## Content {: #hey-there }
    ... is gathered as --hey-there

    ### Hall of fame! {: #hall-of-fame }
    This will be a false negative: the id is considered equivalent to the content,
    and this id will be ignored.
    ```
    """


    ignored_ids: List[str] = []
    """
    If defined, each string will be an html id that will be ignored when gathering and checking
    addresses. Example of definition:

    ```yaml
    plugins:
        - mkdocs-addresses:
            ignored_ids:            # or: ignored_ids: ["subtitle", "skip-this-id"]
                - subtitle
                - skip-this-id
    ```

    Note:
        Ids starting with double underscores will always be ignored (because some plugins use
        them for their own purpose).
    """


    ignored_classes: List[str] = []
    """
    If defined, each string will be an html class that will be ignored when gathering and
    checking addresses. Example of definitions:

    ```yaml
    plugins:
        - mkdocs-addresses:
            ignored_classes:        # or: ignored_classes: ["class-name-1", "non-gathered"]
                - class-name-1
                - non-gathered
    ```

    Note:
        The class "headerlink" will always be skipped (this allows to ignore the permalinks
        generated by the `toc` markdown extension).
    """


    inclusions: List[str] = []
    """
    Slash separated paths, relative to the cwd, that must point to directories containing the
    files you may use for "inclusions" with the `pymdownx.snippets` markdown extension, using:
    `--<8--`.

    If defined, each directory will be added to the list of watched directories, and their
    content will be recursively explored: the plugin will build the code snippets to
    include those files in the docs pages. See [TODO](TODO).

    Example of included snippet:

    `--8<-- "path_from_cwd_to_included_file.with_extension"`

    Note:
        These files are not supposed to be in the `docs_dir` folder in the first place. If they
        are, mkdocs will complain about files not included in the nav anyway.
    """


    links_white_list: List[str] = []
    """
    List of links and/or ids that will ignored when gathering the references, and also when
    checking the addresses. For example:

    ```yaml
    plugins:
        - mkdocs-addresses:
            links_white_list:        # or   links_white_list: ["/media/toto/local_file", "toto"]
                - /media/toto/local_file
                - toto
    ```
    """


    links_white_list_pattern: str = "https?://|ftps?://|file:///|www\\."
    """
    Regex string: all addresses or identifiers that will
    [`re.match`](https://docs.python.org/3/library/re.html#re.match){: target=_blank } with it will be ignored.

    This allows to use absolute addresses, external links, or any other weird case you could
    imagine, so that the plugin doesn't raise an error for them.
    """


    more_verbose: bool = False
    """
    Controls the verbosity level of the plugin, increasing it slightly, without increasing the
    verbosity level of mkdocs logger itself.

    If mkdocs is run in verbose mode, this option is ignored and the verbose mode also applies
    to the plugin.
    """


    plugin_off: bool = False
    """
    If true, completely deactivate the plugin. This may allow to speed up the serve steps if needed.
    """


    use_vsc: bool = True
    """
    Controls the kind of file that will be dumped by the plugin.

    * If true, a VSC `.code-snippets` file will be created at the end of the `on_post_build` event,
    at the location defined by the [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
    option.
    * If false, the plugin still works the same, but you will have to work without the code snippets.
    So the plugin generates a `.txt` file containing all the gathered references and showing what
    the target for each of them.

    Note:
        Keep in mind that this option determines the kind of file used for the
        [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
        option, meaning that, if you assigned a filename for this option, its extension has to
        match with the value of the `use_vsc` option.

        See the section above, explaining the
        [`dump_snippets_file`][mkdocs_addresses.config_plugin.PluginOptions.dump_snippets_file]
        option.
    """


    verify_only: List[str] = []
    """
    If items are defined, the correctness of the addresses will be checked only in those
    markdown files. All other operations are done normally.

    The location must slash separated path, relative to the docs_dir (and _not_ to the cwd).
    For example, to only check "docs/subdir/blabla.md, use:

    ```yaml
    plugins:
        - mkdocs-addresses:
            verify_only:
                - subdir/blabla.md
    ```
    """








PLUGIN_MARK = "VSC-REF"

DUMP_OPTIONS = tuple('normal only none'.split())
NORMAL, DUMP_ONLY, NO_DUMP = DUMP_OPTIONS
assert PluginOptions.dump_action in DUMP_OPTIONS, "Invalid plugin setup"




# Config types definitions...:

ConfigErrors   = List[Tuple[str,bool,str,Optional[Exception]]]
ConfigWarnings = List[Tuple[str,str]]
FatalCbk       = Callable





class AddressAddressesConfig(Config):

    activate_cache = C.Type(bool, default=PluginOptions.activate_cache)

    dump_action = C.Choice(DUMP_OPTIONS, default=PluginOptions.dump_action)

    dump_snippets_file = C.Type(str, default='')      # Automatically overridden at validation time

    external_links_file = C.Type(str, default=PluginOptions.external_links_file)

    fail_fast = C.Type(bool, default=PluginOptions.fail_fast)

    imgs_extension_pattern = C.Type(str, default=PluginOptions.imgs_extension_pattern)

    ignore_auto_headers = C.Type(bool, default=PluginOptions.ignore_auto_headers)

    ignored_ids = C.ListOfItems(C.Type(str), default=PluginOptions.ignored_ids)

    ignored_classes = C.ListOfItems(C.Type(str), default=PluginOptions.ignored_classes)

    inclusions = C.ListOfItems(C.Type(str), default=PluginOptions.inclusions)

    links_white_list = C.ListOfItems(C.Type(str), default=PluginOptions.links_white_list)

    links_white_list_pattern = C.Type(str, default=PluginOptions.links_white_list_pattern)

    more_verbose = C.Type(bool, default=PluginOptions.more_verbose)

    plugin_off = C.Type(bool, default=PluginOptions.plugin_off)

    use_vsc = C.Type(bool, default=PluginOptions.use_vsc)

    verify_only = C.ListOfItems(C.File(exists=True), default=PluginOptions.verify_only)



    #----------------------------------------------



    def validate_and_process(self, config:MkDocsConfig):
        """ Performs the basic, then extras validations on each property, and also apply the
            post conversions to the data structures that need it.
            Add on the fly the needed fields from the mkdocs config.
        """

        # Pre-conversions:
        #-----------------

        if not self.dump_snippets_file:
            self.dump_snippets_file = PluginOptions.dump_file_vsc if self.use_vsc else PluginOptions.dump_file_txt


        # Perform "post" conversions:       (yeah, "post"... lol...)
        #----------------------------

        maybe_abs = path_manager.to_os(config['docs_dir'])
        self.uni_docs_dir = maybe_abs.absolute().relative_to(Path.cwd())

        for prop in 'docs_dir  use_directory_urls'.split():
            setattr(self, prop, config[prop])


        post_conversions: Tuple[Callable[[str],Any], str] = [
            (re.compile, 'imgs_extension_pattern  links_white_list_pattern'),
            (set,        'ignored_ids  ignored_classes  links_white_list  verify_only  inclusions'),
        ]
        for conversion,props in post_conversions:
            for prop in props.split():
                value = getattr(self, prop)
                try:
                    post = conversion(value)
                    setattr(self, prop, post)
                except Exception as e:                              # pylint: disable=all
                    e.args = ( f"{ prop }: { e.args[0] }",)
                    raise

        self.ignored_classes.add('headerlink')      # this avoids to consider mkdocs permalinks in headers, when used

        # More specific validations:
        #---------------------------

        self.__validate_inclusions_dir()
        self.__validate_links_white_list_pattern()
        self.__validate_external_links_file()
        self.__validate_dump_snippets_file()
        self.__validate_verify_only_md_files()
        self.__validate_vsc_and_dump_filename_consistency()



    #----------------------------------------------

    def __check_not_in_docs(self, prop:str, path:str):
        rel = os.path.relpath(path, self.uni_docs_dir)
        if not rel.startswith('..'):
            raise AddresserConfigError(
                f"{prop}: {path!r} should not be inside the docs_dir directory"
            )


    def __validate_inclusions_dir(self):
        self.inclusions = sorted(map( path_manager.to_os, self.inclusions))
        oops = [location for location in self.inclusions if not location.is_dir() ]
        if oops:
            raise AddresserConfigError(
                f"'inclusions' should be a list of directories, but found invalid paths: ({ oops !r})"
            )

        for path in self.inclusions:
            self.__check_not_in_docs('inclusions', path)


    def __validate_links_white_list_pattern(self):
        if not self.links_white_list_pattern.pattern:      # this is now a pattern, not a string anymore!
            raise AddresserConfigError(
                "links_white_list_pattern should never be an empty string. Note that not using at "
                "least the default pattern will definitely cause problems..."
            )


    def __validate_external_links_file(self):
        if not self.external_links_file:
            return

        self.external_links_file = p = path_manager.to_os(self.external_links_file)
        if not p.is_file() or not p.suffix=='.md':
            raise AddresserConfigError(
                "'external_links_file' is configured, but is not an existing markdown file "
                f'("{ self.external_links_file }")'
            )
        self.__check_not_in_docs('external_links_file', self.external_links_file)


    def __validate_dump_snippets_file(self):
        self.dump_snippets_file = path_manager.to_os(self.dump_snippets_file)
        self.__check_not_in_docs('dump_snippets_file', self.dump_snippets_file)


    def __validate_vsc_and_dump_filename_consistency(self):
        snip_file:Path   = self.dump_snippets_file
        vsc_and_snippets = self.use_vsc and snip_file.suffix=='.code-snippets'
        not_vsc_and_txt  = not self.use_vsc and snip_file.suffix=='.txt'
        if not (vsc_and_snippets or not_vsc_and_txt):
            raise AddresserConfigError(
                "Inconsistent configuration:\n"
                f"   use_vsc: {self.use_vsc}\n"
                f"   dump_snippets_file: {self.dump_snippets_file}"
            )


    def __validate_verify_only_md_files(self):
        invalids = [ file for file in self.verify_only
                          if not path_manager.to_os(file).suffix=='.md']
        if invalids:
            raise AddresserConfigError(
                "All options for `verify_only` should be valid markdown files, relative to the cwd.\n"
                +"Invalid entries:" + "".join('\n    '+file for file in invalids)
            )





class ConfigDescriptor:
    """ Dynamic relay data descriptor, to articulate the plugin and its configuration """

    prop: str

    def __set_name__(self, _, prop:str):
        self.prop = prop

    def __get__(self, obj:'AddressAddressesPlugin', _:type):
        return getattr(obj.config, self.prop)

    def __set__(self, obj:'AddressAddressesPlugin', value:Any):
        # setter needed to make this a data descriptor, but should never be used.
        raise InvalidOperationError(
            "Config properties should never be reassigned from the plugin instance."
        )
