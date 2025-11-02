# Athle Tracker Frontend

Modern Next.js 14 frontend for the Athle Tracker application.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: TanStack Query (React Query)
- **Authentication**: NextAuth.js
- **HTTP Client**: Axios

## Project Structure

```
frontend/
├── app/                  # Next.js App Router
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page
│   └── globals.css      # Global styles
├── components/          # React components
│   ├── ui/             # shadcn/ui components
│   └── ...             # Custom components
├── lib/                # Utility functions
│   └── utils.ts        # Class name merger for Tailwind
├── types/              # TypeScript type definitions
│   └── index.ts        # Shared types
├── public/             # Static assets
└── package.json        # Dependencies

```

## Getting Started

### Installation

```bash
# Install dependencies
npm install

# Install shadcn/ui components (when needed)
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
# ... etc
```

### Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

### Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Features

### Layout
- Full-width header with gradient background
- Left sidebar (collapsible)
- Central content area
- Responsive design

### Pages
- **Dashboard**: KPIs, podiums, recent alerts
- **Rankings**: Current rankings with filters
- **Favorites**: Favorite athletes management
- **Alerts**: Notification center
- **Admin**: Event management, user management, scraping

### Authentication
- Login/logout
- Role-based access (admin/user)
- Protected routes
- JWT tokens

## API Integration

The frontend communicates with the FastAPI backend through:
- Base URL: `http://localhost:8000/api`
- Proxy configured in `next.config.mjs`
- TanStack Query for data fetching and caching

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
```

## Code Quality

- **ESLint**: Configured with Next.js rules
- **TypeScript**: Strict mode enabled
- **Prettier**: (Optional) Add for code formatting

## Design System

Using shadcn/ui components based on:
- Radix UI primitives
- Tailwind CSS utility classes
- CSS variables for theming
- Class Variance Authority for variants

## Contributing

1. Keep code clean and DRY
2. Use TypeScript strictly
3. Document components with JSDoc
4. Follow Next.js App Router conventions
5. Ensure responsive design
