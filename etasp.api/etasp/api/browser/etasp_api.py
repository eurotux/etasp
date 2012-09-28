from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from AccessControl import ClassSecurityInfo
from App.config import getConfiguration
import time
from Acquisition import aq_inner
import json


class ETASPApiView(BrowserView):
    """ ETASP Api View """
    render = ViewPageTemplateFile('etasp_api.pt')

    security = ClassSecurityInfo()
    def __init__(self, context, request):
        super(ETASPApiView,self).__init__(context, request)

    def __call__(self):
        return self.render()

    def getInstanceMetadata(self):
        """ return instance metadata"""

        pm = getattr(self.context, 'portal_migration')
        result = {} 
        versions = {}
        versions = pm.coreVersions()      
        result['python_version'] = versions['Python']
        result['zope_version'] = versions['Zope']
        result['plone_version'] = versions['Plone'] 
        if versions['Debug mode'] == 'Yes':
            result['debug_mode'] = True
        else:
            result['debug_mode'] = False

        result['instance_home'] = getConfiguration().instancehome
        result['http_port'] = self.getPort()
        result['uptime'] = self.process_time(_when=None)
        result['etasp_version'] = self.getETASPVersion()

        result_json = json.dumps(result)

        response = self.request.RESPONSE
        setheader = response.setHeader
        setheader('Content-Length', 1)
        setheader('Content-Type', 'application/json; charset=utf-8')

        
        return result_json


    def getPort(self):
        """ return zope port """

        from asyncore import socket_map
        for k,v in socket_map.items():
            # this is only an approximation
            if hasattr(v, 'port'):
                type = str(getattr(v, '__class__', 'unknown'))
                port = v.port
        return port


    process_start = int(time.time())
    def process_time(self, _when=None):
        """ Time from which the service was started """

        if _when is None:
            _when = time.time()
        s = int(_when) - self.process_start
        return s

    def getETASPVersion(self):
        """ return etasp.setup version"""

        pq = getattr(self.context, 'portal_quickinstaller')
        products = pq.listInstalledProducts()
        version = ''   
        for product in products:
            if product['id'] == 'etasp.setup':
                version = product['installedVersion']        
        return version


    def getDatabaseInfo(self):
        """ Returns information about the database """

        context = aq_inner(self.context)
        result = {}
        storage = {}
        filestorage = {}
        filestorage['path'] = context._p_jar.db().getName()
        filestorage['size'] = context._p_jar.db().getSize()
        storage['filestorage'] = filestorage
        #result['tcp_port'] = 8100 SEE sortKey
        result['tcp_port'] = self.get_port()
        result['storage'] = storage


        result_json = json.dumps(result)

        response = self.request.RESPONSE
        setheader = response.setHeader
        setheader('Content-Length', 1)
        setheader('Content-Type', 'application/json; charset=utf-8')


        return result_json



    def getResourceUsage(self):
        """ return information about the resources """

        result = { "memory": "61788","busythreads": 3,}

        result['threads'] = getConfiguration().zserver_threads
        result_json = json.dumps(result)

        response = self.request.RESPONSE
        setheader = response.setHeader
        setheader('Content-Length', 1)
        setheader('Content-Type', 'application/json; charset=utf-8')


        return result_json


    def pack(self):
        """ Instruction to initiate the process of pack from the database """
        context = aq_inner(self.context)
        context._p_jar.db().pack()
        info = context._p_jar.db()._storage.undoInfo()
        result = {}
        if info == []:
            result['status'] = 1
        else:
            result['status'] = 0 
#        return context._p_jar.db().pack()

        result_json = json.dumps(result)

        response = self.request.RESPONSE
        setheader = response.setHeader
        setheader('Content-Length', 1)
        setheader('Content-Type', 'application/json; charset=utf-8')
        return result_json


    def conf(self):
        return getConfiguration()    


    def get_port(self):
        """Return a port that is not in use.
        """
        context = aq_inner(self.context)
        addr = context._p_jar.db()._storage._server_addr
        addr_sep = addr.split(',')
        addr_port = addr_sep[1]
        addr_port = addr_port.replace(')','')
        addr_port = addr_port.replace(' ','')
        return int(addr_port)
