
import re
from typing import Generator, Set, NamedTuple, TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import Tag

from mkdocs_addresses.toolbox import extract_external_links_refs_in_md


from .addresses_checker import AddressKind
from .vsc_auto_completion_handler import RefKind


if TYPE_CHECKING:
    from mkdocs_addresses.addresses_plugin import AddressAddressesPlugin



class SoupTag(NamedTuple):
    tag: Tag
    attr: str
    kind: RefKind
    identifier: str



TR_FR_TABLE = str.maketrans(
    "àâäéèêëîïôöùûüç",
    "aaaeeeeiioouuuc"
)

def kebabize_fr(msg:str):
    ke     = msg.lower().translate(TR_FR_TABLE)
    purged = re.sub(r'&(amp|lt|gt);|[^a-z0-9_ -]+', '', ke)
    bab    = re.findall(r'\w+', purged)
    return '-'.join(bab)



class PluginSoupExcludingCodes(BeautifulSoup):
    """ Personalized version of the BeautifulSoup parser, it will ignore the tags that are
        contained in <code> tags.

        Takes the plugin as argument in the constructor so that it can extract the configuration
        data from it.
    """

    __codes: Set[Tag]
    __plugin: 'AddressAddressesPlugin'


    def __init__(self, html:str, plugin:'AddressAddressesPlugin'):
        super().__init__(html, features="html.parser")
        self.__codes = [*super().find_all('code')]
        self.__plugin = plugin



    def decompose_header_to_kebab(self, header:Tag):
        """ Takes an header tag (<h...>) and converts it to its string content, by removing
            all the unwanted children.

            WARNING: THIS IS MUTATING THE TREE!
        """
        for child in header:
            if isinstance(child,Tag) and "headerlink" in child.get('class',''):
                child.decompose()

        stripped   = header.get_text()
        keb_header = kebabize_fr(stripped)
        return keb_header



    def find_all(self,*a,**kw) -> Set[Tag] :
        candidates = super().find_all(*a,**kw)
        exclusions = { tag for code in self.__codes
                           for tag in code.find_all(*a,**kw) }

        # Filter output as list, and not using sets, to keep the iteration order consistent
        # in other parts of the program:
        return [ cnd for cnd in candidates if cnd not in exclusions ]



    def get_tags_with_ids(self):
        """ Extract all the tags in the html content that:
                - Contain an id attribute (potentially defined on the fly by mkdocs: headers!)
                - Are not in a <code> tag
                - Compliant with the current plugin configuration (ignored ids and classes,
                  white lists, ...)
        """
        return self.find_all(
            id=self.html_id_to_gather,
            class_=self.html_class_to_gather,
        )


    def gen_targeted_addresses_data(self) -> Generator[SoupTag,None,None]:
        """ Explore an html content, searching for links href and images src addresses,
            and yield the corresponding tag with some other informations.
            Note: anchors definitions are skipped.
        """
        links = self.find_all('a', class_=self.html_class_to_gather)
        imgs  = self.find_all('img')

        targeted_tags = (
            (links, 'href', AddressKind.HREF),
            (imgs,  'src',  AddressKind.SRC),
        )
        for tags,attr,kind in targeted_tags:
            for tag in tags:
                if not tag.has_attr(attr):
                    continue
                identifier = tag[attr]
                if not self.is_identifier_or_link_to_ignore(identifier):
                    yield SoupTag(tag, attr, kind, identifier)




    def is_identifier_or_link_to_ignore(self, id_or_address:str):
        """ Check if the given identifier or address must be ignored or not """
        return (
           id_or_address in self.__plugin.links_white_list
           or id_or_address in self.__plugin.ignored_ids
           or self.__plugin.links_white_list_pattern.match(id_or_address)
        )


    def html_class_to_gather(self, class_:str):
        if not class_:
            return True
        kls   = set(class_.split())
        inter = self.__plugin.ignored_classes & kls
        return not inter



    def html_id_to_gather(self, html_id:str):
        return (
            html_id is not None
            and not html_id.startswith('__')
            and not self.is_identifier_or_link_to_ignore(html_id)
        )



    def destroy_codes(self):
        """ Mutate the current instance, removing all the <code> tags """
        for code in self.__codes:
            code.decompose()

    def get_external_refs_in_codes(self):
        """ Generate all the external references that are in code tags (hence, have not been
            modified in the html)
        """
        return (
            id_ for code in self.__codes
                for id_ in extract_external_links_refs_in_md(code.get_text())
        )