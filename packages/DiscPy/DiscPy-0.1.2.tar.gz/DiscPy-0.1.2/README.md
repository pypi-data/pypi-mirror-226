# DiscPy

A python wrapper for the Discuit API.

Thanks to Snocrash and headzoo for sorting out authentication.


## Installation

#### Pip

```
pip install DiscPy
```
KNOWN ISSUE with utilising after this install. This is my first attempt at a package, and it has missed off the "rest_adapater" file. I currently cannot push more updates.

#### Alternative:

Clone the repo and import disc_api.py 

## Basic usage:
```
from DiscPy.disc_api import DiscuitAPI 
api = DiscuitAPI()
api.get_all_posts()
```
or if cloned:
```
from disc_api import DiscuitAPI
```


## **Methods:**

### Authentication
```
api.authenticate(username, password)
```
Will need to be called prior to any POST/PUT/DELETE methods.


### Posts
```
api.get_all_posts()
```
Returns a list of post objects (as seen on discuit.com/home)
GET request.

```
api.get_post_by_id(post_id)
```
Returns a post object by public ID.
GET request.

```
api.get_post_comments(post_id)
```
Returns a list of comment objects by public post ID.
GET request.

```
api.create_post(type, title, community, body, link)
```
Creates a post of given type in given community, with title, body and link.
Type should be either text, image, or link.
Community is the direct name, i.e. "General" (case sensitive)
POST request.

```
api.delete_post(post_id, delete_as, delete_content)
```
Deletes a post by ID. Delete_as is relevant for moderators, otherwise leave it be. 
Delete_content checks if the body should be deleted as well as the post (defaults to True)
DELETE request.

```
api.vote_post(post_id, upvote)
```
Votes on a post by ID (not public ID). If Upvote == True, it will be up. 
POST request.

### Comments

```
api.create_comment(post_id, body, parent_comment_id)
```
Creates a comment on given post. If parent_comment_id is supplied, it will be a reply.
POST request.

```
api.delete_comment(post_id, comment_id, delete_as)
```
Deletes a comment on a post by ID's. delete_as is the same as for delete_post.
DELETE request.

### Community
```
api.get_communites()
```
Returns a list of all communities as community objects.

```
api.get_community_by_id(id)
```
Returns a community object by ID. 
(TODO - add by name)

```
api.get_community_rules(community_id)
```
Returns a list of Rule objects by community ID.

```
api.get_community_mods(community_id)
```
Returns a list of User objects who moderate the community

```
api.get_community_posts(community_id)
```
Returns a list of post objects by community ID

### User

```
api.get_user_by_username(username)
```
Returns a user object by username.

```
api.get_auth_user
```
Returns a User object for the currently authenticated user.

## Objects

These are taken from the documentation supplied by Previnder. My implementation is snake case, e.g. email_confirmed_at, rather than CamelCase.

### User

```js
{
    "id": string, 
    "username": string,
    "email": string, // Could be null
    "emailConfirmedAt": time, // Could be null
    "aboutMe": string, // Could be null
    "points": int,
    "isAdmin": bool,
    "noPosts": int, // Post count of the user
    "noComments": int, // Comment count of the user
    "createdAt": time,
    "deletedAt": time, // Could be null
    "isBanned": bool, // Bool
    "bannedAt": time, // Could be null
    "notificationsNewCount": int, // Number of new notifications the user has
    
    // The list of communities that the user moderates. Could be null. This
    // field is not always populated.
    "moddingList": string[]
}
```

### Post

```js
{
    "id": string, 
    "publicId": string, // The value in https://discuit.net/gaming/post/{publicId}/
    "type": string, // One of "text", "image", "link"

    "userId": string, // Id of the author.
    "username": string, // Username of the author.

    // In what capacity the post was created. One of "normal", "admins", "mods".
    // For "speaking officialy" as a mod or an admin.
    "userGroup": string,

    "userDeleted": bool, // Indicated whether the author's account is deleted 
    "isPinned": bool,
    "communityId": string, // The id of the community the post is posted in
    "communityName": string, // The name of that community

    "title": string,
    "body": string, // Body of the post (only valid for text-posts)

    // Only valid for link-posts. Could be null.
    "link": {}

    "locked": bool,
    "lockedBy": string, // Who locked the post. Could be null.
    "lockedByGroup": string, // One of "admins" or "mods". Could be null.
    "lockedAt": time, // Could be null

    "upvotes": int,
    "downvotes": int,
    "hotness": int, // For ordering posts by 'hot'

    "createdAt": time,
    "editedAt": time, // Last edited time. Could be null.
    
    // Either the post created time or, if there are comments on the post, the
    // time the most recent comment was created at.
    "lastActivityAt": time,

    "deleted": bool,
    "deletedAt": time, // Could be null
    "deletedBy": string, // Id of the user who deleted the post. Could be null.
    "deletedAs": string, // One of "normal", "admins", "mods". Could be null.

    // If true, the body of the post and all associated links or images are
    // deleted.
    "deletedContent": bool,

    "deletedContentAs": string,  // One of "normal", "admins", "mods". Could be null.

    "noComments": int, // Comment count

    "commments": Comment[], // Comments of the post. This field is not always populated.
    "commentsNext": string, // Pagination cursor. Could be null.

    // Indicated whether the authenticated user has voted. If not authenticated,
    // the value is null.
    "userVoted": bool,
    "userVotedUp": bool, // Indicates whether the authenticated user's vote is an upvote.

    "community": {} // The community object of the post. Not always populated.
}
```

### Community

```js
{
    "id": string,
    "userId": string, // Id of the user who created the community
    "name": string,
    "nsfw": bool, // Indicates whether the community hosts NSFW content
    "about": string, // Could be null
    "noMembers": int, // Member count
    "proPic": Image,
    "bannerImage": {},
    "createdAt": time,
    "deletedAt": time, // Could be null

    "isDefault": bool, // This field is not always populated

    "userJoined": bool, // Indicates whether the authenticated user is a member
    "userMod": bool, // Indicates whether the authenticated user is a moderator

    "mods": User[] // An array of User objects. This field is not always populated.

    "rules": CommunityRule[], // Array of CommunityRule. This field is not always populated

    "reportDetails": {
      "noReports": int, // Total reports count
      "noPostReports": int, // Reported posts count
      "noCommentReports": int, // Reported comments count
    }, // This field is not always populated
}
```

### CommunityRule

```js
{
  "id": int,
  "rule": string,
  "description": string, // Could be null
  "communityId": string,
  "zIndex": int, // Determines rule ordering, with lower at top
  "createdBy": string,
  "createdAt": time
}
```

### Comment

```js
{
  "id": string,
  "postId": string,
  "postPublicId": string,
  "communityId": string,
  "communityName": string,
  "userId": string,
  "username": string,

  // The capacity in which the comment was created.
  "userGroup": string, // One of "normal", "admins", "mods".
  "userDeleted": bool, // Indicates whether the author account is deleted
  "parentId": string, // Parent comment id. Could be null.
  "depth": int, // Top-most comments have a depth of 0
  "noReplies": int, // Total number of replies
  "noDirectReplies": int, // Number of direct replies

  // Comment ids of all direct ancestor comments starting from the top-most
  // comment.
  "ancestors": string[], // Array of string. Could be null.

  "body": string, // Comment body
  "upvotes": int,
  "downvotes": int,
  "createdAt": time,
  "editedAt": time, // Last edit time. Could be null.

  "deletedAt": time, // Comment deleted time. Could be null.

  // User id of the person who deleted the comment.
  "deletedBy": string, // Could be null

  // In what capacity the comment was deleted.
  "deletedAs": string, // One of "normal", "admins", "mods". Could be null.

  // Indicated whether the authenticated user has voted. If not authenticated,
  // the value is null.
  "userVoted": bool,
  "userVotedUp": bool, // Indicates whether the authenticated user's vote is an upvote

  "postDeleted": bool, // Indicates whether the post the comment belongs to is deleted

  // If the post is deleted, in what capacity.
  "postDeletedAs": string // One of "normal", "admins", "mods".
}
```
