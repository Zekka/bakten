from primitive import irc_message_representation, MessageType

"""
Conventions:
    A field referring to a target user will always be called 'user'
    A field referring to a target server will always be called 'server'
    A field referring to a target channel will always be called 'channel'
    A field referring to a target that is either a user or a channel will
        be called 'target'.
    A field containing text to be displayed for other users will be called
        'text'.
"""

@irc_message_representation
class PassMessage(MessageType("pass", ["password"])):
    """
    If the user wants to use a password, then this *must* be the first
    message the user sends.
    """
    pass

@irc_message_representation
class NickMessage(MessageType("nick", ["nickname"])):
    """
    Sets the user's nickname or changes the existing one.

    Can be used if the session is still unregistered.
    """
    pass

@irc_message_representation
class UserMessage(MessageType("user", ["user", "modes", "unused", "realname"])):
    """
    Specifies introductory information about a user. It is used to register
    the session.
    """
    @classmethod
    def create(cls):
        return cls([None, 0, "*", None])

@irc_message_representation
class OperMessage(MessageType("oper", ["name", "password"])):
    """
    Allows a user to request oper status from the server, provided that the
    name and password are correct.
    """
    pass

@irc_message_representation
class ModeMessage(MessageType("mode", ["target", "modes", "params"])):
    """
    Allows a user to attempt to set his modes or the modes of a channel.

    TODO: Find a spec for the mode string and implement readers/writers.
    """
    pass

@irc_message_representation
class ServiceMessage(MessageType("service", ["nickname", "reserved1",
    "distribution", "type", "reserved2", "info"])):
    """
    Instructs the server to register a new service.

    Probably won't implement a special create() that blanks those reserved
    fields.
    """
    pass

@irc_message_representation
class QuitMessage(MessageType("quit", ["text"])):
    """
    Quits from the IRC server.

    The server acknowledges this with an ERROR response.
    """
    pass

@irc_message_representation
class SQuitMessage(MessageType("squit", ["server", "text"])):
    """
    Instructs a server to terminate itself with extreme prejudice.
    """
    pass

@irc_message_representation
class JoinMessage(MessageType("join", ["channel", "key"])):
    """
    Joins a channel.

    The RFC specifies a syntax for multiple channels or multiple keys, but I'm
    not going to acknowledge it in the client.
    """
    pass

@irc_message_representation
class PartMessage(MessageType("part", ["channel", "text"])):
    """
    Leaves a channel.

    There's a notation similar to the above for parting multiple channels, too
    but let's let it go unacknowledged for now.
    """
    pass

@irc_message_representation
class TopicMessage(MessageType("topic", ["channel", "text"])):
    """
    Sets the topic of a channel, or else retrieves it if no new one is
    specified.
    """
    pass

@irc_message_representation
class NamesMessage(MessageType("names", ["channel", "server"])):
    """
    Lists the names inside a channel. If no channel is specified, lists
    all the names in all the channels. If a target server is specified, the
    request will be forwarded to that server.

    It's possible to specify multiple channels as in JOIN, but that notation
    isn't dealt with here.
    """
    pass

@irc_message_representation
class ListMessage(MessageType("list", ["channel", "server"])):
    """
    Retrieves a list of channels and their topics. Same channel/target
    semantics as NAMES.

    It's possible to specify multiple channels as in JOIN, but that notation
    isn't dealt with here.
    """
    pass

@irc_message_representation
class InviteMessage(MessageType("invite", ["user", "channel"])):
    """
    Invites the user of the given nickname to join the specified channel.
    """
    pass

@irc_message_representation
class KickMessage(MessageType("kick", ["channel", "user", "text"])):
    """
    Kicks a user.
    
    It's possible to specify a list of users but we don't do that here.
    """
    pass

@irc_message_representation
class PrivmsgMessage(MessageType("privmsg", ["target", "text"])):
    """
    Sends a message to a user or channel.
    """
    pass

@irc_message_representation
class NoticeMessage(MessageType("notice", ["target", "text"])):
    """
    Sends a notice to a user or channel.
    """
    pass

@irc_message_representation
class MOTDMessage(MessageType("motd", ["server"])):
    """
    Requests the message of the day of the given server, or the current one if
    none is specified.
    """
    pass

@irc_message_representation
class LUsersMessage(MessageType("lusers", ["mask", "server"])):
    """
    Gets statistics about the IRC network. If no parameters are specified, then
    the information will apply to the whole network. If a mask is specified
    (mask parameter) then the information will apply only to the specified
    server. If a target server is specified, then the target server will
    generate the reply.
    """
    pass

@irc_message_representation
class VersionMessage(MessageType("version", ["server"])):
    """
    Queries the server about its version. If a server is specified, that server
    will be queried instead.
    """
    pass

@irc_message_representation
class StatsMessage(MessageType("stats", ["query", "target"])):
    """
    Queries certain statistics of certain servers in a way I don't really
    understand.
    """
    pass

@irc_message_representation
class LinksMessage(MessageType("links", ["server", "mask"])):
    """
    Asks a server which servernames it is aware of. The returned list must
    match the mask if it was passed - if no mask was given it will simply
    return the list.

    If a remote server is given, the links command is forwarded to that server
    instead.
    """
    pass

@irc_message_representation
class ConnectMessage(MessageType("connect", ["server", "port", "other"])):
    """
    Asks a server to connect to another server.
    """
    pass

@irc_message_representation
class TraceMessage(MessageType("trace", ["server"])):
    """
    Queries the server for more information you honestly don't care about.
    """
    pass

@irc_message_representation
class AdminMessage(MessageType("admin", ["server"])):
    """
    Queries the server about its administrator if one is specified; otherwise
    it queries the current server.
    """
    pass

@irc_message_representation
class InfoMessage(MessageType("info", ["server"])):
    """
    Seriously. Just guess.
    """
    pass

@irc_message_representation
class ServlistMessage(MessageType("servlist", ["mask", "type"])):
    pass

@irc_message_representation
class SQueryMessage(MessageType("squery", ["user", "text"])):
    """
    According to the RFC, the only way to send a text message to a server, with
    similar semantics to PRIVMSG.

    (This is a blatant lie.)
    """
    pass

@irc_message_representation
class WhoMessage(MessageType("squery", ["mask"])):
    """
    Generates a query returning a list of information matching the parameter
    given by the client. The server knows more than you do.
    """
    pass

@irc_message_representation
class WhoIsMessage(MessageType("whois", ["user", "mask"])):
    """
    Queries information abuot a particular user.
    """
    pass

@irc_message_representation
class WhoWasMessage(MessageType("whowas", ["user", "count", "server"])):
    """
    Asks about the past sessions of a given nickname. Returns up to the
    specified number of replies.
    """
    pass

@irc_message_representation
class PingMessage(MessageType("ping", ["server", "server2"])):
    """
    Tests whether the client or server at the other end of the connection is
    active.

    When this is received, the server at the other end of the ping (or the
    server parameter) *must* receive a reply or else the connection will
    drop.
    """
    pass

@irc_message_representation
class PongMessage(MessageType("pong", ["server", "server2"])):
    """
    Replies to a PING message.
    """
    pass

@irc_message_representation
class ErrorMessage(MessageType("error", ["text"])):
    """
    Informs a client or server of a serious or fatal error.

    Response to QUIT.
    """
    pass

@irc_message_representation
class AwayMessage(MessageType("away", ["text"])):
    """
    Marks a user away and permits them to set an automatic reply string.
    """
    pass

@irc_message_representation
class RehashMessage(MessageType("rehash", [])):
    """
    Requests that the server reprocess its configuration file.
    """
    pass

@irc_message_representation
class DieMessage(MessageType("die", [])):
    """
    Requests that the server shut down.
    """
    pass

@irc_message_representation
class RestartMessage(MessageType("restart", [])):
    """
    Requests that the server restart.
    """
    pass

@irc_message_representation
class SummonMessage(MessageType("summon", ["user", "server", "channel"])):
    """
    Sends a message to a user on a host running an IRC server, asking them
    to join IRC.
    """
    pass

@irc_message_representation
class UsersMessage(MessageType("users", ["server"])):
    """
    Returns a list of users logged onto a server.
    """
    pass

@irc_message_representation
class WallopsMessage(MessageType("wallops", ["text"])):
    """
    Sends a message to all users who currently have the +w usermode.
    """
    pass

@irc_message_representation
class UserHostMessage(MessageType("userhost",
    ["nick", "nick2", "nick3", "nick4", "nick5"])):
    """
    Returns a list of information about each listed nickname.
    """
    pass

@irc_message_representation
class IsOnMessage(MessageType("ison",
    ["nick", "nick2", "nick3", "nick4", "nick5"])):
    """
    Checks which of the nicks in the given list are online.
    """
    pass

def NumericReply(number, name):
    g = MessageType(str(number), ["user", ":text"])
    g.__name__ = name + "Reply"
    return g

def ErrorReply(number, name):
    g = MessageType(str(number), ["user", ":text"])
    g.__name__ = name + "Err"
    return g

WelcomeReply                = NumericReply("001", "Welcome")
YourHostReply               = NumericReply("002", "YourHost")
CreatedReply                = NumericReply("003", "Created")
MyInfoReply                 = NumericReply("004", "MyInfo")
BounceReply                 = NumericReply("005", "Bounce")
    # TODO: May want to respond to this - asks a client to reconnect to a new
    # server
UserHostReply               = NumericReply("302", "UserHost")
IsOnReply                   = NumericReply("303", "IsOn")
AwayReply                   = NumericReply("301", "AwayReply")
UnawayReply                 = NumericReply("305", "UnawayReply")
NowAwayReply                = NumericReply("306", "NowAwayReply")
WhoIsUserReply              = NumericReply("311", "WhoIsUser")
WhoIsServerReply            = NumericReply("312", "WhoIsServer")
WhoIsOperatorReply          = NumericReply("313", "WhoIsOperator")
WhoIsIdleReply              = NumericReply("317", "WhoIsIdle")
EndOfWhoIsReply             = NumericReply("318", "EndOfWhoIs")
WhoIsChannelsReply          = NumericReply("319", "WhoIsChannels")
WhoWasUserReply             = NumericReply("314", "WhoWasUser")
EndOfWhoWasReply            = NumericReply("369", "EndOfWhoWas")
ListStartReply              = NumericReply("321", "ListStart") # obsolete
ListReply                   = NumericReply("322", "List")
ListEndReply                = NumericReply("323", "ListEnd")
OriginalOpIsReply           = NumericReply("325", "OriginalOpIs")
ChannelModeIsReply          = NumericReply("324", "ChannelModeIs")
NoTopicReply                = NumericReply("331", "NoTopic")
TopicReply                  = NumericReply("332", "Topic")
InvitingReply               = NumericReply("334", "Inviting")
SummoningReply              = NumericReply("342", "Summoning")
InviteListReply             = NumericReply("346", "InviteList")
EndOfInviteListReply        = NumericReply("347", "EndOfInviteList")
ExceptListReply             = NumericReply("348", "ExceptList")
EndOfExceptListReply        = NumericReply("349", "EndOfExceptList")
VersionReply                = NumericReply("351", "Version")
WhoReply                    = NumericReply("352", "Who")
NamesReply                  = NumericReply("353", "Names")
    # TODO: This one is listed as 'namreply' in the docs
    # but that seems wrong.
EndOfNamesReply             = NumericReply("366", "EndOfNames")
LinksReply                  = NumericReply("364", "Links")
EndOfLinksReply             = NumericReply("365", "EndOfLinks")
BanListReply                = NumericReply("367", "BanList")
EndOfBanListReply           = NumericReply("368", "EndOfBanList")
InfoReply                   = NumericReply("371", "Info")
EndOfInfoReply              = NumericReply("374", "EndOfInfo")
MotdStartReply              = NumericReply("375", "MotdStart")
MotdReply                   = NumericReply("372", "MotdReply")
EndOfMotdReply              = NumericReply("376", "EndOfMotd")
YoureOperReply              = NumericReply("381", "YoureOper")
RehashingReply              = NumericReply("382", "RehashingReply")
YoureServiceReply           = NumericReply("383", "YoureService")
TimeReply                   = NumericReply("391", "Time")
UsersStartReply             = NumericReply("392", "UsersStart")
UsersReply                  = NumericReply("393", "Users")
EndOfUsersReply             = NumericReply("394", "EndOfUsers")
NoUsersReply                = NumericReply("395", "NoUsers")
TraceLinkReply              = NumericReply("200", "TraceLink")
TraceConnectingReply        = NumericReply("201", "TraceConnecting")
TraceHandshakeReply         = NumericReply("202", "TraceHandshake")
TraceUnknownReply           = NumericReply("203", "TraceUnknown")
TraceOperatorReply          = NumericReply("204", "TraceOperator")
TraceUserReply              = NumericReply("205", "TraceUser")
TraceServerReply            = NumericReply("206", "TraceServer")
TraceServiceReply           = NumericReply("207", "TraceService")
TraceNewTypeReply           = NumericReply("208", "TraceNewType")
TraceClassReply             = NumericReply("209", "TraceClass")
TraceReconnectReply         = NumericReply("210", "TraceReconnect")
TraceLogReply               = NumericReply("261", "TraceLog")
TraceEndReply               = NumericReply("262", "TraceEnd")
StatsLinkInfoReply          = NumericReply("211", "StatsLinkInfo")
StatsCommandsReply          = NumericReply("212", "StatsCommands")
EndOfStatsReply             = NumericReply("219", "EndOfStats")
StatsUptimeReply            = NumericReply("242", "StatsUptime")
StatsOnlineReply            = NumericReply("243", "StatsOnline")
UModeIsReply                = NumericReply("221", "UModeIs")
ServListReply               = NumericReply("234", "ServList")
EndOfServListReply          = NumericReply("235", "EndOfServList")
LUserClientReply            = NumericReply("251", "LUserClient")
LUserOpReply                = NumericReply("252", "LUserOp")
LUserUnknownReply           = NumericReply("253", "LUserUnknown")
LUserChannelsReply          = NumericReply("254", "LUserChannels")
LUserMeReply                = NumericReply("255", "LUserMe")
AdminMeReply                = NumericReply("256", "AdminMe")
AdminLoc1Reply              = NumericReply("257", "AdminLoc1")
AdminLoc2Reply              = NumericReply("258", "AdminLoc2")
AdminEmailReply             = NumericReply("259", "AdminEmail")
TryAgainReply               = NumericReply("263", "TryAgain")

# Error replies
NoSuchNickErr               = ErrorReply("401", "NoSuchNick")
NoSuchServerErr             = ErrorReply("402", "NoSuchServer")
NoSuchChannelErr            = ErrorReply("403", "NoSuchChannel")
CannotSendToChannelErr      = ErrorReply("404", "CannotSendToChannel")
TooManyChannelsErr          = ErrorReply("405", "TooManyChannels")
WasNoSuchNickErr            = ErrorReply("406", "WasNoSuchNick")
TooManyTargetsErr           = ErrorReply("407", "TooManyTargets")
NoSuchServiceErr            = ErrorReply("408", "NoSuchService")
NoOriginErr                 = ErrorReply("409", "NoOrigin")
NoRecipientErr              = ErrorReply("411", "NoRecipient")
NoTextToSendErr             = ErrorReply("412", "NoTextToSend")
NoTopLevelErr               = ErrorReply("413", "NoTopLevel")
WildTopLevelErr             = ErrorReply("414", "WildTopLevel")
BadMaskErr                  = ErrorReply("415", "BadMask")
UnknownCommandErr           = ErrorReply("421", "UnknownCommand")
NoMotdErr                   = ErrorReply("422", "NoMotd")
NoAdminInfoErr              = ErrorReply("423", "NoAdminInfo")
FileErr                     = ErrorReply("424", "File")
NoNicknameGivenErr          = ErrorReply("431", "NoNicknameGiven")
ErroneousNicknameErr        = ErrorReply("432", "ErroneousNickname")
NicknameInUseErr            = ErrorReply("433", "NicknameInUse")
NickCollisionErr            = ErrorReply("436", "NickCollision")
UnavailableResourceErr      = ErrorReply("437", "UnavailableResource")
UserNotInChannelErr         = ErrorReply("441", "UserNotInChannel")
NotInChannelErr             = ErrorReply("442", "NotInChannel")
UserInChannelErr            = ErrorReply("443", "UserInChannel")
NotLoggedInErr              = ErrorReply("444", "NotLoggedIn")
SummonDisabledErr           = ErrorReply("445", "SummonDisabled")
UsersDisabledErr            = ErrorReply("446", "UsersDisabled")
NotRegisteredErr            = ErrorReply("451", "NotRegistered")
NeedMoreParamsErr           = ErrorReply("461", "NeedMoreParams")
AlreadyRegisteredErr        = ErrorReply("462", "AlreadyRegistered")
NoPermissionsForHostErr     = ErrorReply("463", "NoPermissionsForHost")
PasswordMismatchErr         = ErrorReply("464", "PasswordMismatch")
YoureBannedErr              = ErrorReply("465", "YoureBanned")
YouWillBeBannedErr          = ErrorReply("466", "YouWillBeBanned")
KeyAlreadySetErr            = ErrorReply("467", "KeyAlreadySet")
ChannelIsFullErr            = ErrorReply("471", "ChannelIsFull")
UnknownModeErr              = ErrorReply("472", "UnknownMode")
InviteOnlyChannelErr        = ErrorReply("473", "InviteOnlyChannel")
BannedFromChannelErr        = ErrorReply("474", "BannedFromChannel")
BadChannelKeyErr            = ErrorReply("475", "BadChannelKey")
BadChannelMaskErr           = ErrorReply("476", "BadChannelMask")
ModesNotSupportedErr        = ErrorReply("477", "ModesNotSupported")
BanListFullErr              = ErrorReply("478", "BanListFull")
NoPrivilegesErr             = ErrorReply("481", "NoPrivileges")
ChannelOperatorPrivilegesNeededErr = ErrorReply("482",
        "ChannelOperatorPrivilegesNeeded")
CantKillServerErr           = ErrorReply("483", "CantKillServer")
RestrictedConnectionErr     = ErrorReply("484", "RestrictedConnection")
OriginalOperatorPrivilegesNeededErr = ErrorReply("485",
        "OriginalOperatorPrivilegesNeeded")
NoOLinesForHostErr          = ErrorReply("491", "NoOLinesForHost")
UModeUnknownFlagErr         = ErrorReply("501", "UModeUnknownFlag")
UsersDontMatchErr           = ErrorReply("502", "UsersDontMatch")

class JustConnected(object):
    """
    A fake IRCMessage used to trigger events that occur on connection for
    Services.
    """
    pass

class AboutToLeave(object):
    """
    A fake IRCMessage used to trigger events that occur when connection is
    ending for Services.
    """
    pass
