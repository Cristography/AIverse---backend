# AIverse - API Documentation

Base URL: `http://127.0.0.1:8000/api/v1/`

All API responses are in JSON format.

---

## Authentication

Uses JWT (JSON Web Tokens) for authentication.

### Register

**POST** `/auth/register/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepass123",
  "password2": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

---

### Login

**POST** `/auth/login/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "username": "johndoe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

---

### Refresh Token

**POST** `/auth/token/refresh/`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "new-access-token-here"
}
```

---

### Get Current User Profile

**GET** `/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "AI enthusiast",
  "avatar": "http://127.0.0.1:8000/media/avatars/profile.jpg",
  "website": "https://example.com",
  "preferred_language": "en",
  "theme_preference": "dark",
  "total_prompts": 15,
  "total_comments": 42,
  "total_bookmarks": 8
}
```

---

### Update Profile

**PUT/PATCH** `/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Updated bio",
  "website": "https://johndoe.com",
  "preferred_language": "ar"
}
```

---

## Tags

### List All Tags

**GET** `/tags/`

**Query Parameters:**
- `search` - Search by tag name

**Response (200 OK):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Copywriting",
      "slug": "copywriting",
      "description": "Prompts for writing and content creation",
      "prompt_count": 25
    }
  ]
}
```

---

## Prompts

### List All Prompts

**GET** `/prompts/`

**Query Parameters:**
- `type` - Filter by type: `text` or `image`
- `tags` - Filter by tag slugs (comma-separated): `?tags=copywriting,seo`
- `search` - Search in title and body
- `ordering` - Sort by: `created_at`, `-created_at`, `upvotes`, `-upvotes`
- `page` - Page number
- `page_size` - Items per page (max 100)

**Response (200 OK):**
```json
{
  "count": 150,
  "next": "http://127.0.0.1:8000/api/v1/prompts/?page=2",
  "previous": null,
  "total_pages": 8,
  "current_page": 1,
  "results": [
    {
      "id": "uuid-here",
      "title": "Create a Marketing Campaign",
      "slug": "create-a-marketing-campaign",
      "body": "Create a {{campaign_type}} campaign for {{product}}...",
      "type": "text",
      "image": null,
      "author": {
        "id": "uuid",
        "username": "johndoe",
        "email": "john@example.com"
      },
      "tags": [
        {"id": 1, "name": "Marketing", "slug": "marketing"}
      ],
      "upvotes": 42,
      "user_has_upvoted": false,
      "is_bookmarked": false,
      "comment_count": 12,
      "created_at": "2025-10-31T20:15:00Z",
      "updated_at": "2025-10-31T20:15:00Z"
    }
  ]
}
```

---

### List Text Prompts Only

**GET** `/prompts/text/`

Same as `/prompts/` but filtered to `type=text`

---

### List Image Prompts Only

**GET** `/prompts/image/`

Same as `/prompts/` but filtered to `type=image`

---

### Get Single Prompt

**GET** `/prompts/<slug>/`

**Response (200 OK):**
```json
{
  "id": "uuid-here",
  "title": "Create a Marketing Campaign",
  "slug": "create-a-marketing-campaign",
  "body": "Create a {{campaign_type}} campaign for {{product}} targeting {{audience}}. The tone should be {{tone}} and include {{call_to_action}}.",
  "type": "text",
  "image": null,
  "author": {
    "id": "uuid",
    "username": "johndoe",
    "email": "john@example.com",
    "avatar": "http://..."
  },
  "tags": [
    {"id": 1, "name": "Marketing", "slug": "marketing"},
    {"id": 2, "name": "Copywriting", "slug": "copywriting"}
  ],
  "upvotes": 42,
  "user_has_upvoted": true,
  "is_bookmarked": false,
  "comment_count": 12,
  "views": 245,
  "created_at": "2025-10-31T20:15:00Z",
  "updated_at": "2025-10-31T20:15:00Z"
}
```

---

### Create Prompt

**POST** `/prompts/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data (if uploading image)
Content-Type: application/json (if text only)
```

**Request Body (Text Prompt):**
```json
{
  "title": "Email Subject Line Generator",
  "body": "Generate 10 email subject lines for {{product}} targeting {{audience}}",
  "type": "text",
  "tags": [1, 2, 3]
}
```

**Request Body (Image Prompt):**
```
FormData with:
- title: "Cyberpunk Character"
- body: "A cyberpunk character in {{setting}} with {{style}}"
- type: "image"
- image: <file>
- tags: [4, 5]
```

**Response (201 Created):**
Same as GET single prompt response.

---

### Update Prompt

**PUT/PATCH** `/prompts/<slug>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Permissions:** Only the author can update their prompt.

---

### Delete Prompt

**DELETE** `/prompts/<slug>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Permissions:** Only the author or admin can delete.

**Response (204 No Content)**

---

### Upvote/Downvote Prompt

**POST** `/prompts/<slug>/vote/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "action": "upvote"  // or "downvote" to remove vote
}
```

**Response (200 OK):**
```json
{
  "upvotes": 43,
  "user_has_upvoted": true
}
```

---

## Comments

### List Comments for Prompt

**GET** `/prompts/<slug>/comments/`

**Response (200 OK):**
```json
{
  "count": 12,
  "results": [
    {
      "id": "uuid",
      "author": {
        "id": "uuid",
        "username": "johndoe",
        "avatar": "http://..."
      },
      "body": "Great prompt! Very useful.",
      "created_at": "2025-10-31T21:00:00Z",
      "updated_at": "2025-10-31T21:00:00Z",
      "is_edited": false,
      "can_edit": false,
      "can_delete": false
    }
  ]
}
```

---

### Create Comment

**POST** `/prompts/<slug>/comments/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "body": "This is a helpful prompt!"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "author": {...},
  "body": "This is a helpful prompt!",
  "created_at": "2025-10-31T21:05:00Z"
}
```

---

### Update Comment

**PUT/PATCH** `/comments/<id>/`

**Permissions:** Only comment author can update.

---

### Delete Comment

**DELETE** `/comments/<id>/`

**Permissions:** Comment author, prompt author, or admin can delete.

---

## Bookmarks

### List User's Bookmarks

**GET** `/bookmarks/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "count": 8,
  "results": [
    {
      "id": "uuid",
      "prompt": {
        "id": "uuid",
        "title": "...",
        "slug": "...",
        "type": "text"
      },
      "created_at": "2025-10-31T20:00:00Z"
    }
  ]
}
```

---

### Toggle Bookmark

**POST** `/prompts/<slug>/bookmark/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "bookmarked": true,  // or false if removed
  "message": "Bookmark added"  // or "Bookmark removed"
}
```

---

## News, Blogs, Tools

All follow similar patterns (read-only for users):

### List Items

**GET** `/news/` or `/blogs/` or `/tools/`

### Get Single Item

**GET** `/news/<slug>/` or `/blogs/<slug>/` or `/tools/<slug>/`

**Response structure same as prompts but without upvotes/bookmarks.**

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation error",
  "details": {
    "email": ["This field is required."]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Rate Limiting

Currently no rate limiting in development.

In production:
- 100 requests per hour for authenticated users
- 20 requests per hour for anonymous users

---

## Pagination

All list endpoints support pagination:

- `?page=2` - Get page 2
- `?page_size=50` - Get 50 items per page (max 100)

Response includes:
- `count` - Total items
- `next` - URL to next page (null if last page)
- `previous` - URL to previous page (null if first page)
- `total_pages` - Total number of pages
- `current_page` - Current page number
- `results` - Array of items
