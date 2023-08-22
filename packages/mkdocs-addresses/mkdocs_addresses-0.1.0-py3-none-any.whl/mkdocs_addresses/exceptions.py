from mkdocs.exceptions import PluginError


class AddresserError(PluginError):
    """ Generic mkdocs-addresses exception. Extends PluginError """



#------------------------------------------------



class AbortError(AddresserError):
    """ Thrown at the face of mkdocs logger... :p
        (see addresses_auto_log final try/except block)
    """


class AddresserConfigError(AddresserError):
    """ Plugin config related error """



class InvalidOperationError(AddresserConfigError):
    """ Don't to that... """



class DumpOnlyError(AddresserError):
    """ Generic mkdocs-addresses exception. """



class MarkdownLinkError(AddresserError):
    """ Generic mkdocs-addresses exception. """



#------------------------------------------------



class AbstractAddressError(AddresserError):
    """ Path/address related errors. Extends AddresserError """


class NonAbsoluteAddressError(AbstractAddressError):
    """ Address is not considered absolute. """

class NonRelativeAddressError(AbstractAddressError):
    """ Address is not considered relative (no leading dot) """

class LeadingSlashAddressError(AbstractAddressError):
    """ Addresses with leading slash are not allowed """

class TrailingSlashAddressError(AbstractAddressError):
    """ Addresses with trailing slash """

class NotAnImageAddressError(AbstractAddressError):
    """ The address isn't considered the one of an image. """

class NoMoveUpDirOnNonIndexPageUrlsAsDirAddressError(AbstractAddressError):
    """ In a non index.md file while using use_directory_urls, the address does not start
        with a "../"
    """




class AnchorAddressError(AbstractAddressError):
    """ Invalid anchor found in an Address """


class ImageWithAnchorError(AnchorAddressError):
    """ Images src attribute should never contain an anchor """

class TooManyAnchorsError(AnchorAddressError):
    """ More than one hashtag in the address """

class AnchorUnknownError(AnchorAddressError):
    """ Anchor not referenced anywhere """

class AnchorNotInPageError(AnchorAddressError):
    """ Anchor not referenced in the current page """

class EmptyAnchorError(AnchorAddressError):
    """ Trailing anchor without identifier (spot {: # wrong } errors) """



#------------------------------------------------



class IdentifierError(AddresserError):
    """ References/Id related errors """


class InvalidIdentifierError(IdentifierError):
    """ A reference identifier is invalid """

class DuplicateIdentifierError(IdentifierError):
    """ An identifier has already been registered """

class UnknownIdentifierError(IdentifierError):
    """ Unknown identifier """

class UnknownExternalLinkIdentifierError(IdentifierError):
    """ Unknown identifier """



class OutdatedReferenceError(IdentifierError):
    """ Identifier used in some document, but that isn't defined anywhere anymore (note: can occur
        only for unchanged documents that were cached and so, not checked on this build, while the
        reference they are using has been deleted in another file).
    """



#-------------------------------------------------

class ConcurrentPluginError(Exception):
    """ Using only for testing purpose, ensuring that pytest doesn't run in // """
