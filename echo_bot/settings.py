from configparser import SafeConfigParser


class Settings():
    config = SafeConfigParser()
    config.read("settings.ini")

    def write_changes(self):
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)
            config_file.close()

    def get_config(self, key, default=None):
        return self.config.get("DEFAULT", key, fallback=default)

    def set_config(self, key, value):
        value = str(value)
        self.config.set("DEFAULT", key, value)
        self.write_changes()
