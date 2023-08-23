from enum import StrEnum


class Metrics:
    def __init__(
            self,
            size: int = None,
            ascent: int = None,
            descent: int = None,
            x_height: int = None,
            cap_height: int = None,
    ):
        self.size = size
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height

    @property
    def line_height(self) -> int:
        return self.ascent - self.descent

    def check_ready(self):
        if self.size is None:
            raise Exception("Missing metrics: 'size'")
        if self.ascent is None:
            raise Exception("Missing metrics: 'ascent'")
        if self.descent is None:
            raise Exception("Missing metrics: 'descent'")


class StyleName(StrEnum):
    LIGHT = 'Light'
    NORMAL = 'Normal'
    REGULAR = 'Regular'
    MEDIUM = 'Medium'
    BOLD = 'Bold'
    HEAVY = 'Heavy'


class SerifMode(StrEnum):
    SERIF = 'Serif'
    SANS_SERIF = 'Sans-Serif'


class WidthMode(StrEnum):
    MONOSPACED = 'Monospaced'
    PROPORTIONAL = 'Proportional'


class MetaInfos:
    def __init__(
            self,
            version: str = '0.0.0',
            family_name: str = None,
            style_name: str = StyleName.REGULAR,
            serif_mode: SerifMode = None,
            width_mode: WidthMode = None,
            manufacturer: str = None,
            designer: str = None,
            description: str = None,
            copyright_info: str = None,
            license_info: str = None,
            vendor_url: str = None,
            designer_url: str = None,
            license_url: str = None,
            sample_text: str = None,
    ):
        self.version = version
        self.family_name = family_name
        self.style_name = style_name
        self.serif_mode = serif_mode
        self.width_mode = width_mode
        self.manufacturer = manufacturer
        self.designer = designer
        self.description = description
        self.copyright_info = copyright_info
        self.license_info = license_info
        self.vendor_url = vendor_url
        self.designer_url = designer_url
        self.license_url = license_url
        self.sample_text = sample_text

    def check_ready(self):
        if self.version is None:
            raise Exception("Missing meta infos: 'version'")
        if self.family_name is None:
            raise Exception("Missing meta infos: 'family_name'")
        if self.style_name is None:
            raise Exception("Missing meta infos: 'style_name'")
