from Products.Five import BrowserView
from iw.fss.config import ZCONFIG
from collective.flowplayer import metadata_extraction as metaex
from collective.flowplayerstreaming.config import MAX_WIDTH, MAX_HEIGHT
import os


class RTSPView(BrowserView):
    """ View for video player """

    def href(self):
        """ """
        # FIXME
        return 'static/' + self.context.UID() + '_video_file'

    def scale(self):
        """ """
        path_dir = ZCONFIG.storagePathForSite('/')
        path = os.path.join(path_dir)
        filename = self.context.UID() + '_video_file'
        metadata = metaex.parse_file(path_dir + '/' + filename)
        height, width = metaex.scale_from_metadata(metadata)

        if MAX_WIDTH < width:
            height = int(height*MAX_WIDTH / width)
            width = MAX_WIDTH

        return "height: %dpx; width: %dpx;" % (height, width)
