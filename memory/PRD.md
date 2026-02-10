# Valentine Proposal Website - PRD

## Original Problem Statement
Create a single-page responsive website for Valentine's Day proposals with:
- UUID-based unique links for each proposal
- Customizable valentine name, message, and character selection
- Mischievous "No" button that evades clicks
- Heart confetti celebration on acceptance
- Floating hearts background
- Pastel pink and white theme

## User Personas
1. **Proposal Creator**: Someone who wants to send a creative, fun Valentine's proposal
2. **Valentine Recipient**: The person receiving the proposal link

## Core Requirements (Static)
- [x] UUID-based unique links stored in MongoDB
- [x] Lottie/GIF character animation (Panda, Bear, Bunny)
- [x] Custom name and message input
- [x] Character selection
- [x] Floating hearts background
- [x] Pastel pink/white theme
- [x] Mobile responsive design

## What's Been Implemented (Feb 10, 2026)

### Backend (FastAPI)
- POST /api/proposals - Create new proposal with UUID
- GET /api/proposals/:id - Fetch proposal by UUID
- PATCH /api/proposals/:id - Update acceptance status
- MongoDB storage for all proposals

### Frontend (React + Tailwind)
- **Homepage**: Create proposal form with name, message, character selection
- **Proposal Page**: Interactive proposal with Yes/No buttons
- **FloatingHearts**: Animated background hearts
- **CharacterAnimation**: Lottie/image character display
- **ProposalCard**: Main proposal component with all interactions

### Mischievous "No" Button Logic
- Moves to random position on hover (desktop) and touch (mobile)
- Changes text on click: "Are you sure?", "Really?", "Think again!"
- Yes button grows 20% larger on each No attempt
- No button disappears after 3 attempts

### Celebration
- Heart confetti animation using canvas-confetti
- "Yay! See you on the 14th!" message
- Large pulsing heart icon

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Core proposal creation flow
- [x] Unique link generation
- [x] Proposal display page
- [x] Yes/No interaction logic
- [x] Confetti celebration

### P1 (Important)
- [ ] Add more character options (cat, dog, etc.)
- [ ] Custom celebration messages
- [ ] Social sharing buttons (WhatsApp, Twitter)
- [ ] QR code generation for links

### P2 (Nice to Have)
- [ ] Sound effects on interactions
- [ ] Multiple theme options (dark mode, different colors)
- [ ] Proposal templates
- [ ] Analytics dashboard for creators

## Next Tasks
1. Add social sharing buttons for easy link distribution
2. Implement QR code generation for proposals
3. Add more character/animation options
4. Consider adding audio for the celebration

## Tech Stack
- Frontend: React, Tailwind CSS, Framer Motion, canvas-confetti
- Backend: FastAPI, MongoDB, Motor
- Hosting: Emergent Platform
