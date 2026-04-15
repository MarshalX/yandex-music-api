__version__ = '2.2.0'
__license__ = 'GNU Lesser General Public License v3 (LGPLv3)'
__copyright__ = 'Copyright (C) 2019-2026 Ilya (Marshal) <https://github.com/MarshalX>'

from .base import ClientType, YandexMusicObject, YandexMusicModel, JSONType, MapTypeToDeJson

from .settings import Settings
from .permission_alerts import PermissionAlerts
from .experiments import Experiments

from .account.status import Status
from .account.account import Account
from .account.plus import Plus
from .account.alert_button import AlertButton
from .account.alert import Alert
from .account.user_settings import UserSettings
from .account.non_auto_renewable import NonAutoRenewable
from .account.deactivation import Deactivation
from .account.operator import Operator
from .account.subscription import Subscription
from .account.price import Price
from .account.product import Product
from .account.auto_renewable import AutoRenewable
from .account.renewable_remainder import RenewableRemainder
from .account.passport_phone import PassportPhone
from .account.permissions import Permissions

from .album.album import Album
from .album.album_trailer import AlbumTrailer
from .album.label import Label
from .album.track_position import TrackPosition
from .album.trailer_info import TrailerInfo
from .album.deprecation import Deprecation

from .artist.artist import Artist
from .artist.artist_albums import ArtistAlbums
from .artist.artist_link import ArtistLink
from .artist.artist_tracks import ArtistTracks
from .artist.brief_info import BriefInfo
from .artist.counts import Counts
from .artist.description import Description
from .artist.link import Link
from .artist.ratings import Ratings
from .artist.stats import Stats
from .artist.vinyl import Vinyl

from .concert.concert_min_price import ConcertMinPrice
from .concert.concert_cashback import ConcertCashback
from .concert.concert_event_info import ConcertEventInfo
from .concert.concert import Concert
from .concert.artist_concerts import ArtistConcerts

from .playlist.case_forms import CaseForms
from .playlist.made_for import MadeFor
from .playlist.user import User
from .playlist.contest import Contest
from .playlist.custom_wave import CustomWave
from .playlist.open_graph_data import OpenGraphData
from .playlist.brand import Brand
from .playlist.play_counter import PlayCounter
from .playlist.playlist_id import PlaylistId
from .playlist.tag import Tag
from .playlist.tag_result import TagResult
from .playlist.playlist_absence import PlaylistAbsence
from .playlist.playlist import Playlist
from .playlist.playlist_recommendation import PlaylistRecommendations

from .shot.shot_type import ShotType
from .shot.shot_data import ShotData
from .shot.shot import Shot
from .shot.shot_event import ShotEvent

from .tracks_list import TracksList
from .track.major import Major
from .track.licence_text_part import LicenceTextPart
from .track.track_lyrics import TrackLyrics
from .track.lyrics_major import LyricsMajor
from .track.poetry_lover_match import PoetryLoverMatch
from .track.meta_data import MetaData
from .track.normalization import Normalization
from .track.track import Track
from .track.tracks_similar import SimilarTracks
from .track.r128 import R128
from .track.lyrics_info import LyricsInfo

from .feed.generated_playlist import GeneratedPlaylist
from .feed.album_event import AlbumEvent
from .feed.artist_event import ArtistEvent
from .feed.track_with_ads import TrackWithAds
from .feed.day import Day
from .feed.event import Event
from .feed.feed import Feed

from .promo_code_status import PromoCodeStatus
from .download_info import DownloadInfo
from .video import Video

from .search.best import Best
from .search.search import Search
from .search.suggestions import Suggestions
from .search.search_result import SearchResult

from .landing.chart_item import ChartItem
from .landing.play_context import PlayContext
from .landing.track_short_old import TrackShortOld
from .landing.mix_link import MixLink
from .landing.promotion import Promotion
from .landing.block_entity import BlockEntity
from .landing.landing import Landing
from .landing.block import Block
from .landing.landing_list import LandingList
from .landing.chart_info_menu_item import ChartInfoMenuItem
from .landing.chart_info_menu import ChartInfoMenu
from .landing.chart_info import ChartInfo
from .landing.track_id import TrackId
from .landing.chart import Chart
from .landing.play_contexts_data import PlayContextsData
from .landing.personal_playlists_data import PersonalPlaylistsData

from .genre.title import Title
from .genre.images import Images
from .genre.genre import Genre

from .rotor.id import Id
from .rotor.value import Value
from .rotor.enum import Enum
from .rotor.sequence import Sequence
from .rotor.station_data import StationData
from .rotor.discrete_scale import DiscreteScale
from .rotor.ad_params import AdParams
from .rotor.restrictions import Restrictions
from .rotor.rotor_settings import RotorSettings
from .rotor.station import Station
from .rotor.station_tracks_result import StationTracksResult
from .rotor.station_result import StationResult
from .rotor.dashboard import Dashboard

from .supplement.supplement import Supplement
from .supplement.lyrics import Lyrics
from .supplement.video_supplement import VideoSupplement

from .queue.context import Context
from .queue.queue import Queue
from .queue.queue_item import QueueItem

from .wave.wave import Wave
from .wave.wave_agent_entity import WaveAgentEntity
from .wave.wave_agent import WaveAgent
from .wave.similar_entity_data import SimilarEntityData
from .wave.similar_entity_item import SimilarEntityItem

from .content_restrictions import ContentRestrictions
from .like import Like
from .pager import Pager
from .cover import Cover
from .cover_derived_colors import CoverDerivedColors
from .invocation_info import InvocationInfo
from .track_short import TrackShort
from .icon import Icon
from .pin.pin_data import PinData
from .pin.pin import Pin
from .client import Client
from .client_async import ClientAsync


__all__ = [
    'R128',
    'Account',
    'AdParams',
    'Album',
    'AlbumEvent',
    'AlbumTrailer',
    'Alert',
    'AlertButton',
    'Artist',
    'ArtistAlbums',
    'ArtistConcerts',
    'ArtistEvent',
    'ArtistLink',
    'ArtistTracks',
    'AutoRenewable',
    'Best',
    'Block',
    'BlockEntity',
    'Brand',
    'BriefInfo',
    'CaseForms',
    'Chart',
    'ChartInfo',
    'ChartInfoMenu',
    'ChartInfoMenuItem',
    'ChartItem',
    'Client',
    'ClientAsync',
    'ClientType',
    'Concert',
    'ConcertCashback',
    'ConcertEventInfo',
    'ConcertMinPrice',
    'ContentRestrictions',
    'Contest',
    'Context',
    'Counts',
    'Cover',
    'CoverDerivedColors',
    'CustomWave',
    'Dashboard',
    'Day',
    'Deactivation',
    'Deprecation',
    'Description',
    'DiscreteScale',
    'DownloadInfo',
    'Enum',
    'Event',
    'Experiments',
    'Feed',
    'GeneratedPlaylist',
    'Genre',
    'Icon',
    'Id',
    'Images',
    'InvocationInfo',
    'JSONType',
    'Label',
    'Landing',
    'LandingList',
    'LicenceTextPart',
    'Like',
    'Link',
    'Lyrics',
    'LyricsInfo',
    'LyricsMajor',
    'MadeFor',
    'Major',
    'MapTypeToDeJson',
    'MetaData',
    'MixLink',
    'NonAutoRenewable',
    'Normalization',
    'OpenGraphData',
    'Operator',
    'Pager',
    'PassportPhone',
    'PermissionAlerts',
    'Permissions',
    'PersonalPlaylistsData',
    'Pin',
    'PinData',
    'PlayContext',
    'PlayContextsData',
    'PlayCounter',
    'Playlist',
    'PlaylistAbsence',
    'PlaylistId',
    'PlaylistRecommendations',
    'Plus',
    'PoetryLoverMatch',
    'Price',
    'Product',
    'PromoCodeStatus',
    'Promotion',
    'Queue',
    'QueueItem',
    'Ratings',
    'RenewableRemainder',
    'Restrictions',
    'RotorSettings',
    'Search',
    'SearchResult',
    'Sequence',
    'Settings',
    'Shot',
    'ShotData',
    'ShotEvent',
    'ShotType',
    'SimilarEntityData',
    'SimilarEntityItem',
    'SimilarTracks',
    'Station',
    'StationData',
    'StationResult',
    'StationTracksResult',
    'Stats',
    'Status',
    'Subscription',
    'Suggestions',
    'Supplement',
    'Tag',
    'TagResult',
    'Title',
    'Track',
    'TrackId',
    'TrackLyrics',
    'TrackPosition',
    'TrackShort',
    'TrackShortOld',
    'TrackWithAds',
    'TracksList',
    'TrailerInfo',
    'User',
    'UserSettings',
    'Value',
    'Video',
    'VideoSupplement',
    'Vinyl',
    'Wave',
    'WaveAgent',
    'WaveAgentEntity',
    'YandexMusicModel',
    'YandexMusicObject',
    '__copyright__',
    '__license__',
    '__version__',
]
