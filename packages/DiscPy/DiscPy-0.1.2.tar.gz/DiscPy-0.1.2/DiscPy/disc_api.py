import logging
from rest_adapter import RestAdapter
from models import *

class DiscuitAPI:
    def __init__(self, hostname: str = 'discuit.net/api', ssl_verify: bool = True,
                 logger: logging.Logger = None):
        
        self._rest_adapter = RestAdapter(hostname, ssl_verify, logger)

    def authenticate(self, username:str, password:str):
        result = self._rest_adapter.authenticate(username,password)
        return result
    
    def get_all_posts(self) -> Posts:
        """Gets most recent posts, site-wide.

        Returns:
            Posts: A list of Post objects.
        """
        result = self._rest_adapter.get(endpoint='posts')
        posts = Posts(**result.data)
        return posts
    
    def get_community_posts(self, community_id: str) -> Posts:
        """Gets most recent posts by Community ID

        Args:
            community_id (str): The ID of the community to get posts from.

        Returns:
            Posts: A list of Post objects.
        """
        params = {
            "communityId" : community_id
        }

        result = self._rest_adapter.get(endpoint=f'posts', ep_params=params)
        posts = Posts(**result.data)
        return posts
    
    def get_post_by_id(self, post_id: str) -> Post:
        """Get a Post object by Public ID
        Currently returns list of posts, even though its one.

        Args:
            post_id (str): The Public ID of the post (discuit.com/postId)

        Returns:
            Posts: List of Post objects.
        """
        # post ID should be the public ID
        # currently broken, as models are weird
        result = self._rest_adapter.get(endpoint=f'posts/{post_id}')
        post = Post(**result.data)
        return post
    
    def get_post_comments(self, post_id:str) -> Comments: 
        """Get comments on a post by Public ID

        Args:
            post_id (str): The Public ID of the post.

        Returns:
            Comments: A list of Comment objects
        """
        result = self._rest_adapter.get(endpoint=f'posts/{post_id}/comments')
        comments = Comments(**result.data)
        return comments

    def fetch_link_data(self, link: Link):
        link.data = self._rest_adapter.fetch_data(url=link.url)

    def get_communites(self) -> List[Community]:
        """Returns a list of all communities, sitewide

        Returns:
            List[Community]: A list of community objects
        """
        results = self._rest_adapter.get(endpoint='communities')
        communities_list = [Community(**datum) for datum in results.data]
        return communities_list

    def get_community_by_id(self, community_id: str) -> Community:
        """Returns a community object by ID.

        Args:
            community_id (str): The community ID.

        Returns:
            Community: A Community object
        """
        result = self._rest_adapter.get(endpoint=f'communities/{community_id}')
        community = Community(**result.data)
        return community

    def get_community_rules(self, community_id: str) -> List[CommunityRule]:
        """Returns a list of CommunityRule objects for the community ID

        Args:
            community_id (str): ID of community.

        Returns:
            List[CommunityRule]: A List of CommunityRule objects
        """
        result = self._rest_adapter.get(endpoint=f"communities/{community_id}/rules")
        rules_list = [CommunityRule(**datum) for datum in result.data]
        return rules_list

    def get_community_mods(self, community_id: str) -> List[User]:
        """Returns a list of User objects that moderate the community.

        Args:
            community_id (str): Community ID

        Returns:
            List[User]: A list of user objects.
        """
        result = self._rest_adapter.get(endpoint=f"communities/{community_id}/mods")
        mods_list = [User(**datum) for datum in result.data]
        return mods_list

    def get_user_by_username(self, username: str) -> User:
        """Returns a User object by username

        Args:
            username (str): the username of the user

        Returns:
            User: A User object
        """
        result = self._rest_adapter.get(endpoint=f"users/{username}")
        user = User(**result.data)
        return user

    def get_auth_user(self):
        """Returns a User object for the currently authenticated user.

        Returns:
            _type_: _description_
        """
        result = self._rest_adapter.get(endpoint="_user")
        user = User(**result.data)
        return user

    def create_post(self, type: str, title: str, community:str, 
                    body:str = None, url:str = None) -> Post:
        """Creates a post with the supplied args. Returns the Post object.

        Args:
            type (str): Type of post. One of "text", "image", "link".
            title (str): Title of the post
            community (str): Community to post in (common, i.e. "General")
            body (str, optional): Body of the post. Required for text posts. Defaults to None.
            url (str, optional): URL for the post. Required for image and link posts. Defaults to None.

        Returns:
            Post: A Post object of the created post.
        """
        data = {
            "type" : type,
            "title" : title,
            "body" : body,
            "community" : community,
            "url" : url
        }
        result = self._rest_adapter.post(endpoint="posts", data=data)

        post = Post(**result.data)
        return post
    
    def update_post(self, post_id:str, title:str = None, body:str = None, should_lock:bool = False):

        data = {
            "title" : title,
            "body" : body
        }

        result = self._rest_adapter.put(endpoint=f"posts/{post_id}", data=data)
    
    def delete_post(self, post_id:str, delete_as: str = "Normal", delete_content:bool = True) -> Post:
        """Deletes the post by public post_id.

        Args:
            post_id (str): Public Post ID
            delete_as (str, optional): One of 'normal', 'mods', 'admins'. Defaults to Normal.
            delete_content (bool, optional): If True, the body will also be deleted. Defaults to True.

        Returns:
            Post: Post object of deleted post.
        """
        params = {
            "deleteAs" : delete_as,
            "deleteContent" : delete_content
        }

        result = self._rest_adapter.delete(endpoint=f"posts/{post_id}", ep_params=params)

        return Post(**result.data)
    
    def vote_post(self, post_id:str, upvote:bool):
        """Votes on a post by post ID.

        Args:
            post_id (str): ID of the post (not public ID)
            upvote (bool): If True, up, if False, down

        Returns:
            Status Code: The status code of the request.
        """
        params = {
            "postId" : post_id,
            "up" : upvote
        }

        result = self._rest_adapter.post(endpoint="_postVote", data=params)

        return result.status_code

    def create_comment(self, post_id:str, body:str, parent_comment_id:str = None):
        """Creates a comment on given Post ID. If Parent comment ID is supplied, it will be a reply

        Args:
            post_id (str): the ID of the Post
            body (str): Body of the comment
            parent_comment_id (str, optional): ID of the comment to reply to. Defaults to None.

        Returns:
            Comment: Comment object of created comment.
        """
        data = {
            "parentCommentID" : parent_comment_id,
            "body" : body
        }

        result = self._rest_adapter.post(endpoint=f"posts/{post_id}/comments", data=data)

        # Need to modify Comment model, as result.data apparently doesnt give all info
        comment = Comment(**result.data)
        return comment
    
    def delete_comment(self, post_id:str, comment_id:str, delete_as:str = 'Normal'):

        data = {
            "deleteAs" : delete_as
        }

        result = self._rest_adapter.delete(endpoint=f"posts/{post_id}/comments/{comment_id}", data=data)

        return result.status_code
    
    def vote_comment(self, comment_id:str, upvote:bool):
        """Votes on a comment by comment ID.

        Args:
            comment_id (str): ID of the post (not public ID)
            upvote (bool): If True, up, if False, down

        Returns:
            Status Code: The status code of the request.
        """
        data = {
            "commentId" : comment_id,
            "up" : upvote
        }

        result = self._rest_adapter.post(endpoint="_commentVote", data=data)

        return result.status_code