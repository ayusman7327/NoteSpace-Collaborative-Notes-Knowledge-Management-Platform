# NoteSpace

### AI-Powered Collaborative Notes & Knowledge Management Platform

NoteSpace is a full-stack collaborative knowledge management platform designed for creating structured workspaces, organizing nested pages, collaborating with team members, managing documents, and using AI to improve productivity.

It combines a modern React frontend with a FastAPI backend, PostgreSQL database, role-based collaboration, rich-text editing, comments, attachments, version history, and Gemini-powered AI features.

---

## Overview

NoteSpace helps users organize knowledge inside collaborative workspaces.

Users can:

- Create and manage workspaces
- Create nested knowledge pages
- Write rich-text notes
- Auto-save content
- Favorite important pages
- Restore deleted pages
- View previous page versions
- Comment on pages
- Invite workspace members
- Assign Editor and Viewer roles
- Upload page attachments
- Search workspace content
- Use AI for writing and knowledge assistance
- Track workspace activity

---

## Features

### Authentication

- User registration
- User login
- JWT-based authentication
- Protected frontend routes
- Password hashing
- Current-user authentication
- Secure API access

### Workspace Management

- Create workspaces
- Open and manage workspaces
- Workspace owner permissions
- Workspace membership system
- Editor and Viewer roles
- Invite users by email
- Accept or reject workspace invitations
- Cancel pending invitations
- Remove workspace members
- Change member roles
- Leave shared workspaces

### Knowledge Pages

- Create pages
- Create nested pages
- Edit page titles
- Rich-text page editor
- Automatic page saving
- Parent/child page hierarchy
- Soft delete pages
- Restore deleted pages
- Favorite pages
- Track recently opened pages

### Rich Text Editor

NoteSpace uses TipTap for rich-text editing.

Supported editor features include:

- Bold
- Italic
- Headings
- Bullet lists
- Blockquotes
- Code blocks
- Rich HTML content
- Automatic saving

### Version History

- Store previous versions of pages
- View page history
- Restore previous page versions
- Track content changes

### Comments

Users can collaborate using page comments.

Features include:

- Add comments
- Edit own comments
- Delete own comments
- Resolve comments
- Reopen resolved comments
- View page discussions

### Attachments

Users can attach files directly to pages.

Supported file types include:

- PNG
- JPG / JPEG
- WEBP
- PDF
- DOCX
- TXT
- Markdown

Attachment features:

- Click-to-upload
- Drag-and-drop upload
- File size validation
- File type validation
- Open attachments
- Delete attachments
- Attachment metadata
- Maximum file size of 10 MB

### Search

- Search workspace pages
- Filter pages by title
- Quickly navigate knowledge content

### AI Assistant

NoteSpace integrates Gemini AI to provide intelligent writing and knowledge assistance.

AI capabilities include:

- Summarize page content
- Explain content
- Improve writing
- Rewrite text
- Fix grammar
- Generate useful content
- Assist with workspace knowledge

Future AI improvements can include:

- Retrieval-Augmented Generation
- Semantic workspace search
- AI-generated action items
- Context-aware workspace chat
- Vector database integration

### Activity Tracking

NoteSpace includes activity logging support for tracking important workspace actions such as:

- Page creation
- Page updates
- Page deletion
- Page restoration
- Collaboration activity

---

# Tech Stack

## Frontend

- React
- Vite
- JavaScript
- React Router
- Axios
- TipTap
- React Hot Toast
- CSS

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Uvicorn
- Python Multipart
- Psycopg2

## Database

- PostgreSQL
- Alembic migrations

## AI

- Google Gemini API

## Development Tools

- Git
- GitHub
- VS Code
- Postman / FastAPI Swagger
- npm
- pip
- Python Virtual Environment

---

# Project Architecture

```text
NoteSpace/
│
├── backend/
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── app/
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── models/
│   │   │   ├── activity_log.py
│   │   │   ├── attachment.py
│   │   │   ├── comment.py
│   │   │   ├── page.py
│   │   │   ├── page_version.py
│   │   │   ├── tag.py
│   │   │   ├── user.py
│   │   │   ├── workspace.py
│   │   │   ├── workspace_invitation.py
│   │   │   └── workspace_member.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── activity_log_repository.py
│   │   │   ├── attachment_repository.py
│   │   │   ├── comment_repository.py
│   │   │   ├── page_repository.py
│   │   │   ├── page_version_repository.py
│   │   │   ├── tag_repository.py
│   │   │   ├── user_repository.py
│   │   │   ├── workspace_invitation_repository.py
│   │   │   ├── workspace_member_repository.py
│   │   │   └── workspace_repository.py
│   │   │
│   │   ├── routers/
│   │   │   ├── activity_logs.py
│   │   │   ├── ai.py
│   │   │   ├── attachments.py
│   │   │   ├── auth.py
│   │   │   ├── comments.py
│   │   │   ├── pages.py
│   │   │   ├── tags.py
│   │   │   ├── users.py
│   │   │   ├── workspace_invitations.py
│   │   │   ├── workspace_members.py
│   │   │   └── workspaces.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── activity_log.py
│   │   │   ├── attachment.py
│   │   │   ├── comment.py
│   │   │   ├── page.py
│   │   │   ├── tag.py
│   │   │   ├── user.py
│   │   │   ├── workspace.py
│   │   │   ├── workspace_invitation.py
│   │   │   └── workspace_member.py
│   │   │
│   │   ├── services/
│   │   │   ├── activity_log_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── attachment_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── comment_service.py
│   │   │   ├── page_service.py
│   │   │   ├── tag_service.py
│   │   │   ├── workspace_invitation_service.py
│   │   │   ├── workspace_member_service.py
│   │   │   └── workspace_service.py
│   │   │
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── .env
│   ├── alembic.ini
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   │
│   │   ├── api/
│   │   │   ├── attachments.js
│   │   │   ├── axios.js
│   │   │   ├── comments.js
│   │   │   ├── pages.js
│   │   │   ├── search.js
│   │   │   ├── workspaceInvitations.js
│   │   │   ├── workspaceMembers.js
│   │   │   └── workspaces.js
│   │   │
│   │   ├── components/
│   │   │   ├── AIAssistant.jsx
│   │   │   ├── AIAssistant.css
│   │   │   ├── AttachmentsPanel.jsx
│   │   │   ├── AttachmentsPanel.css
│   │   │   ├── CommentsPanel.jsx
│   │   │   ├── CommentsPanel.css
│   │   │   ├── InviteMembersModal.jsx
│   │   │   ├── InviteMembersModal.css
│   │   │   ├── ProtectedRoute.jsx
│   │   │   ├── SearchModal.jsx
│   │   │   ├── SearchModal.css
│   │   │   ├── WorkspaceMembersPanel.jsx
│   │   │   └── WorkspaceMembersPanel.css
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Workspace.jsx
│   │   │   ├── Auth.css
│   │   │   ├── Dashboard.css
│   │   │   └── Workspace.css
│   │   │
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
