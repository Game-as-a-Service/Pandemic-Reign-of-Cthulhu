# Pandemic Reign of Cthulhu

This is the frontend repo of pandemic reign of cthulhu,
written in next.js 13

## Project Structure
In next.js 13, pages are put under /app.
- the app dir root layout is required
- each route is defined by
- - nested folder under app
- - page.js to make the route publicly accessible

- assets
- - here puts the assets use in the frontend game app
- - categorized by type (e.g. investigator, clue-card, etc)

- components
- - common components that are used in the app
- - including investigator card, clue card, the old ones card, etc

- modules (if needed)
- - put the module used only for a certain page in here

- shared
- - put the commonly used constants, type, interface here
- - can also consider putting common state management here (e.g. jotai)

## Getting Started

### How to run the app in local
Example of environment variables will be put as env-file in the directory.
If such file exists, please ensure that the environment variables are set up first before use.

1. install dependencies
```npm run install```

2. run development server
```npm run dev```

The app should be running on http://localhost:3000

/design serves as a design system page for components reference


### How to fix lint
``` npm run lint ```

### How to build
``` npm run build```
