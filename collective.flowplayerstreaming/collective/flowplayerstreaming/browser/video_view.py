from Products.Five import BrowserView
from iw.fss.config import ZCONFIG


class VideoView(BrowserView):
    """ View for video player """

    def href(self):
        """ """
        fss_storage = ZCONFIG.storagePathForSite('/')
        return fss_storage + '/' + self.context.UID() + '_video_file'

    def scale(self):
        """ """
        height = 330
        width = 520
        return "height: %dpx; width: %dpx;" % (height, width)
