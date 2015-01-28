__author__ = 'endru'
import ConfigParser
import ContourFinder as CF

class MyConfig:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.file_name="contourFinder.ini"
        self.config.read(self.file_name)
        self.resolution_w = self.get_number("Camera", "resolution_w", 640)
        self.resolution_h = self.get_number("Camera", "resolution_h", 480)
        self.field_x = self.get_number("Approx", "field_x", 0)
        self.field_y = self.get_number("Approx", "field_y", 0)
        self.field_width= self.get_number("Approx", "field_width", 640)
        self.field_height=self.get_number("Approx", "field_height", 480)
        self.approx_rect_w=self.get_number("Approx", "approx_rect_w", 100)
        self.approx_rect_h=self.get_number("Approx", "approx_rect_h", 120)
        self.threshold = self.get_number("Approx", "threshold", 65)

    def set_resolution(self, resolution_rect):
        """

        :param resolution_rect: CF.Rect
        """
        self.resolution_h = resolution_rect.height
        self.set_number("Camera", "resolution_h", self.resolution_h)
        self.resolution_w = resolution_rect.width
        self.set_number("Camera", "resolution_w", self.resolution_w)

    def set_field(self, field):
        """

        :param field: CF.Field
        """
        self.field_x=field.x
        self.set_number("Approx","field_x",self.field_x)
        self.field_y=field.y
        self.set_number("Approx","field_y",self.field_y)
        self.field_width=field.width
        self.set_number("Approx","field_width",self.field_width)
        self.field_height=field.height
        self.set_number("Approx","field_height",self.field_height)

    def set_approx_rect(self, approx_rect):
        """

        :param approx_rect: CF.Rect
        """
        self.approx_rect_h = approx_rect.height
        self.set_number("Approx", "approx_rect_h", self.approx_rect_h)
        self.approx_rect_w = approx_rect.width
        self.set_number("Approx", "approx_rect_w", self.approx_rect_w)

    def set_threshold(self, threshold):
        """

        :param threshold: int
        """
        self.threshold = threshold
        self.set_number("Approx", "threshold", threshold)

    def set_number(self,section, option, val):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, val)
        self.writeConfig()

    def get_number(self, section, option, default_val=0):
        if self.config.has_section(section):
            if self.config.has_option(section, option):
                return self.config.getint(section, option)
            else:
                self.config.set(section, option, default_val)
                self.writeConfig()
        else:
            self.config.add_section(section)
            self.config.set(section, option, default_val)
            self.writeConfig()
            return default_val

    def writeConfig(self):
        with open(self.file_name, 'wb') as configfile:
            self.config.write(configfile)