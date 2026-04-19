__version__ = '3.1.0b2'
__license__ = 'GNU Lesser General Public License v3 (LGPLv3)'
__copyright__ = 'Copyright (C) 2019-2026 Ilya (Marshal) <https://github.com/MarshalX>'

from .base import ClientType, YandexMusicObject, YandexMusicModel, JSONType, MapTypeToDeJson

from .settings import Settings
from .permission_alerts import PermissionAlerts
from .experiments import Experiments
from .experiment.experiment_detail_value import ExperimentDetailValue
from .experiment.experiment_detail import ExperimentDetail
from .experiment.experiments_details import ExperimentsDetails

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

from .album.album_action_button import AlbumActionButton
from .album.album import Album
from .album.album_similar_entities import AlbumSimilarEntities
from .album.album_trailer import AlbumTrailer
from .album.track_position import TrackPosition
from .trailer_info import TrailerInfo
from .album.deprecation import Deprecation

from .artist.about_artist import ArtistAbout
from .artist.artist import Artist
from .artist.artist_albums import ArtistAlbums
from .artist.artist_clip_data import ArtistClipData
from .artist.artist_clip_item import ArtistClipItem
from .artist.artist_clips import ArtistClips
from .artist.artist_donation_data import ArtistDonationData
from .artist.artist_donation_goal import ArtistDonationGoal
from .artist.artist_donation_item import ArtistDonationItem
from .artist.artist_donations import ArtistDonations
from .artist.artist_info import ArtistInfo
from .artist.artist_link import ArtistLink
from .artist.artist_links import ArtistLinks
from .artist.artist_similar import ArtistSimilar
from .skeleton.skeleton_source import SkeletonSource
from .skeleton.skeleton_view_all_action import SkeletonViewAllAction
from .skeleton.skeleton_block_data import SkeletonBlockData
from .skeleton.skeleton_block import SkeletonBlock
from .skeleton.skeleton_tab import SkeletonTab
from .artist.artist_skeleton import ArtistSkeleton
from .artist.artist_tracks import ArtistTracks
from .artist.artist_trailer import ArtistTrailer
from .artist.artist_trailer_status import ArtistTrailerStatus
from .artist.brief_info import BriefInfo
from .artist.counts import Counts
from .artist.description import Description
from .artist.link import Link
from .artist.ratings import Ratings
from .artist.stats import Stats
from .artist.vinyl import Vinyl

from .clip.clip import Clip
from .clip.clips_will_like import ClipsWillLike

from .concert.concert_min_price import ConcertMinPrice
from .concert.concert_cashback import ConcertCashback
from .concert.concert_event_info import ConcertEventInfo
from .concert.concert import Concert
from .concert.artist_concerts import ArtistConcerts
from .concert.concert_description import ConcertDescription
from .concert.concert_location import ConcertLocation
from .concert.concert_locations import ConcertLocations
from .concert.concert_tab_range import ConcertTabRange
from .concert.concert_tab_config_data import ConcertTabConfigData
from .concert.concert_tab_config import ConcertTabConfig
from .concert.concert_feed_item_data import ConcertFeedItemData
from .concert.concert_feed_item import ConcertFeedItem
from .concert.concert_feed import ConcertFeed
from .concert.concert_info import ConcertInfo
from .concert.concert_skeleton import ConcertSkeleton

from .label.label import Label
from .label.label_albums import LabelAlbums
from .label.label_artists import LabelArtists

from .metatag.metatag_title import MetatagTitle
from .metatag.metatag_sort_by_value import MetatagSortByValue
from .metatag.metatag_leaf import MetatagLeaf
from .metatag.metatag_tree import MetatagTree
from .metatag.metatags import Metatags
from .metatag.metatag import Metatag
from .metatag.metatag_artist_entry import MetatagArtistEntry
from .metatag.metatag_artists import MetatagArtists
from .metatag.metatag_albums import MetatagAlbums
from .metatag.metatag_playlists import MetatagPlaylists

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
from .playlist.playlist_availability import PlaylistAvailability
from .playlist.playlist import Playlist
from .playlist.playlist_recommendation import PlaylistRecommendations
from .playlist.playlist_similar_entities import PlaylistSimilarEntities
from .playlist.playlist_trailer import PlaylistTrailer
from .playlist.playlists_list import PlaylistsList

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
from .track.fade import Fade
from .track.smart_preview_params import SmartPreviewParams
from .track.track_trailer import TrackTrailer
from .track.track_full_info import TrackFullInfo

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

from .music_history.music_history_item_id import MusicHistoryItemId
from .music_history.music_history_context_full_model import MusicHistoryContextFullModel
from .music_history.music_history_item_data import MusicHistoryItemData
from .music_history.music_history_item import MusicHistoryItem
from .music_history.music_history_group import MusicHistoryGroup
from .music_history.music_history_tab import MusicHistoryTab
from .music_history.music_history import MusicHistory
from .music_history.music_history_items import MusicHistoryItems

from .presave.presaves import Presaves

from .content_restrictions import ContentRestrictions
from .credit import Credit
from .credits import Credits
from .device_auth.device_code import DeviceCode
from .device_auth.token import OAuthToken
from .disclaimer import Disclaimer
from .foreign_agent import ForeignAgent
from .like import Like
from .pager import Pager
from .cover import Cover
from .cover_derived_colors import CoverDerivedColors
from .invocation_info import InvocationInfo
from .track_short import TrackShort
from .icon import Icon
from .pin.pin_data import PinData
from .pin.pin import Pin
from .pin.pins_list import PinsList
from .client import Client
from .client_async import ClientAsync


__all__ = [
    'R128',
    'Account',
    'AdParams',
    'Album',
    'AlbumActionButton',
    'AlbumEvent',
    'AlbumSimilarEntities',
    'AlbumTrailer',
    'Alert',
    'AlertButton',
    'Artist',
    'ArtistAbout',
    'ArtistAlbums',
    'ArtistClipData',
    'ArtistClipItem',
    'ArtistClips',
    'ArtistConcerts',
    'ArtistDonationData',
    'ArtistDonationGoal',
    'ArtistDonationItem',
    'ArtistDonations',
    'ArtistEvent',
    'ArtistInfo',
    'ArtistLink',
    'ArtistLinks',
    'ArtistSimilar',
    'ArtistSkeleton',
    'ArtistTracks',
    'ArtistTrailer',
    'ArtistTrailerStatus',
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
    'Clip',
    'ClipsWillLike',
    'Concert',
    'ConcertCashback',
    'ConcertDescription',
    'ConcertEventInfo',
    'ConcertFeed',
    'ConcertFeedItem',
    'ConcertFeedItemData',
    'ConcertInfo',
    'ConcertLocation',
    'ConcertLocations',
    'ConcertMinPrice',
    'ConcertSkeleton',
    'ConcertTabConfig',
    'ConcertTabConfigData',
    'ConcertTabRange',
    'ContentRestrictions',
    'Contest',
    'Context',
    'Counts',
    'Cover',
    'CoverDerivedColors',
    'Credit',
    'Credits',
    'CustomWave',
    'Dashboard',
    'Day',
    'Deactivation',
    'Deprecation',
    'Description',
    'DeviceCode',
    'Disclaimer',
    'DiscreteScale',
    'DownloadInfo',
    'Enum',
    'Event',
    'ExperimentDetail',
    'ExperimentDetailValue',
    'Experiments',
    'ExperimentsDetails',
    'Fade',
    'Feed',
    'ForeignAgent',
    'GeneratedPlaylist',
    'Genre',
    'Icon',
    'Id',
    'Images',
    'InvocationInfo',
    'JSONType',
    'Label',
    'LabelAlbums',
    'LabelArtists',
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
    'Metatag',
    'MetatagAlbums',
    'MetatagArtistEntry',
    'MetatagArtists',
    'MetatagLeaf',
    'MetatagPlaylists',
    'MetatagSortByValue',
    'MetatagTitle',
    'MetatagTree',
    'Metatags',
    'MixLink',
    'MusicHistory',
    'MusicHistoryContextFullModel',
    'MusicHistoryGroup',
    'MusicHistoryItem',
    'MusicHistoryItemData',
    'MusicHistoryItemId',
    'MusicHistoryItems',
    'MusicHistoryTab',
    'NonAutoRenewable',
    'Normalization',
    'OAuthToken',
    'OpenGraphData',
    'Operator',
    'Pager',
    'PassportPhone',
    'PermissionAlerts',
    'Permissions',
    'PersonalPlaylistsData',
    'Pin',
    'PinData',
    'PinsList',
    'PlayContext',
    'PlayContextsData',
    'PlayCounter',
    'Playlist',
    'PlaylistAbsence',
    'PlaylistAvailability',
    'PlaylistId',
    'PlaylistRecommendations',
    'PlaylistSimilarEntities',
    'PlaylistTrailer',
    'PlaylistsList',
    'Plus',
    'PoetryLoverMatch',
    'Presaves',
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
    'SkeletonBlock',
    'SkeletonBlockData',
    'SkeletonSource',
    'SkeletonTab',
    'SkeletonViewAllAction',
    'SmartPreviewParams',
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
    'TrackFullInfo',
    'TrackId',
    'TrackLyrics',
    'TrackPosition',
    'TrackShort',
    'TrackShortOld',
    'TrackTrailer',
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
