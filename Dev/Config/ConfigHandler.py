__author__ = 'endru'
import ConfigParser

class ConfigHandler:
    def __init__(self, file_path):
        self.config = ConfigParser.ConfigParser()
        self.file_name = file_path

    def set_number(self,section, option, val):
        self.set_option(section, option, val)

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

    def get_string(self,section, option, default_val=""):
        if self.config.has_section(section):
            if self.config.has_option(section, option):
                return self.config.get(section, option)
            else:
                self.config.set(section, option, default_val)
                self.writeConfig()
        else:
            self.config.add_section(section)
            self.config.set(section, option, default_val)
            self.writeConfig()
        return default_val

    def get_float(self, section, option, default_val=0.0):
        if self.config.has_section(section):
            if self.config.has_option(section, option):
                return self.config.getfloat(section, option)
            else:
                self.config.set(section, option, default_val)
                self.writeConfig()
        else:
            self.config.add_section(section)
            self.config.set(section, option, default_val)
            self.writeConfig()
            return default_val

    def set_option(self,section, option, val):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, val)
        self.writeConfig()

    def writeConfig(self):
        with open(self.file_name, 'wb') as configfile:
            self.config.write(configfile)