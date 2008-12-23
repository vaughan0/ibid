from ConfigParser import SafeConfigParser
import simplejson

class Config(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        if type(value) == dict:
            self[name] = Config(value)
        else:
            self[name] = value

class StaticConfig(Config):
    def __init__(self):
        local = Config(name='local', type='irc', server='localhost', nick='Ibid', channels=['#cocoontest'])
        atrum = Config(type='irc', server='za.atrum.org', nick='Ibid', channels=['#ibid'])
        jabber = Config(type='jabber', server='jabber.org', ssl=True, jid='ibidbot@jabber.org/source', password='ibiddev')
        myjabber = Config(name='jabber', type='jabber', server='gorven.za.net', ssl=True, jid='ibid@gorven.za.net/source', password='z1VdLdxgunupGSju')
        telnet = Config(type='telnet', port=3000)
        timer = Config(type='timer', step=5)
        
        self.name = 'Ibid'
        self.sources = Config(local=local, atrum=atrum, jabber=jabber, telnet=telnet, clock=timer)
        self.processors = ['core.Addressed', 'irc.Actions', 'core.Ignore', 'admin.ListModules', 'admin.LoadModules', 'basic.Greet', 'info.DateTime', 'basic.SayDo', 'test.Delay', 'basic.Complain', 'core.Responses', 'log.Log']
        self.modules = Config({
                'core.Addressed': Config(names = ['Ibid', 'bot', 'ant']),
                'core.Ignore': Config(ignore = ['NickServ']),
                'ping': Config(type='dbus.Proxy', bus_name='org.ibid.module.Ping', object_path='/org/ibid/module/Ping', pattern='^ping$'),
                'log.Log': Config(logfile='/tmp/ibid.log')})

class FileConfig(Config):
    def __init__(self, filename):
        self.parser = SafeConfigParser()
        self.parser.read(filename)

        for section in self.parser.sections():
            splitted = section.split('.', 1)
            for thing in splitted:
                if thing != 'main':
                    if thing not in dict:
                        dict[thing] = {}
                        dict = dict[thing]
                    for option in self.parser.options(section):
                        value = self.parser.get(section, option)
                        if value.find(',') != -1:
                                value = value.split(',')
                                value = [entry.strip() for entry in value]
                                dict[option] = value
