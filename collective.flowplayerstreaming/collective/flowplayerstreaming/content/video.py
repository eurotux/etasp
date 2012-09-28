from zope.interface import implements
from Products.Archetypes import public as atapi
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeBaseSchema
from iw.fss.FileSystemStorage import FileSystemStorage

from collective.flowplayerstreaming import config
from collective.flowplayerstreaming.interfaces import IVideo


VideoSchema = ATContentTypeBaseSchema.copy() + atapi.Schema((
    atapi.FileField('video_file',
        storage=FileSystemStorage(),
        widget=atapi.FileWidget(
            label = 'Video',
        )
    ),
))


class Video(ATCTContent):
    """ Video content type """

    implements(IVideo)

    portal_type = 'Video'

    schema = VideoSchema

    _at_rename_after_creation = True


atapi.registerType(Video, config.PROJECTNAME)
