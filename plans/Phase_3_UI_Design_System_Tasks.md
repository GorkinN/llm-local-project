# Phase: Evaluate Existing Codebase - Sub-task Checklist

## Setup & Configuration Analysis
- [ ] Read `package.json` - Document all dependencies, devDependencies, and scripts
- [ ] Read `vite.config.js` (or equivalent) - Map out build configuration and plugins
- [ ] Check for environment files (`env`, `.env.*`) - Verify available Node versions and package manager setup
- [ ] Run `npm ls` or `yarn list` - Audit current dependencies and identify any outdated packages

## Component & File Structure Audit
- [ ] Audit `/src/components` directory - List all existing component files with their purposes
- [ ] Read `/src/App.jsx` - Document main app structure and routing setup
- [ ] Check `/src/pages` or similar layout directories - List page/component templates
- [ ] Review `/src/hooks`, `/src/utils`, `/src/services` directories - Catalog shared code
- [ ] Inspect `/public/assets` - Note available images/icons/fonts

## API & Backend Integration
- [ ] Check existing API service files in `/src/services` or `/src/api` folders
- [ ] Identify backend API endpoints by reviewing HTTP client calls (axios, fetch, etc.)
- [ ] List all routes/URLs being called from frontend code
- [ ] Document request/response patterns and data transformation layers

## State Management Assessment
- [ ] Search for any state management libraries (Redux, Zustand, Jotai, React Context) imports
- [ ] Review `/src/store`, `/src/context` directories if present
- [ ] Check component composition for manual state handling patterns
- [ ] Identify global vs. local state usage and scope

## Authentication & Authorization
- [ ] Search codebase for auth-related files or constants (JWT tokens, sessions, cookies)
- [ ] Review API integration endpoints related to login/logout/register
- [ ] Check how user data is stored/managed in UI components
- [ ] Note any authentication headers or token handling approaches

## Styling & Theme
- [ ] Review `/src/styles`, `/src/index.css` files for current styling approach
- [ ] Verify Tailwind CSS configuration and custom theme settings
- [ ] Check for additional CSS modules or styled-components usage

## Documentation & Scripts
- [ ] Verify README exists and contains setup documentation
- [ ] Review `scripts` section in package.json for available dev commands
- [ ] Check for TypeScript configuration if present (`tsconfig.json`)

## Final Assessment Checklist
- [ ] Document any known issues or technical debt flags
- [ ] Summarize overall architecture assessment
- [ ] List recommendations for codebase improvements before proceeding