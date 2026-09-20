// Shared contract. Mirrors data/recipes.json, which is the canonical source.
//
// Do NOT re-declare recipes as a TS constant. Read the JSON in a server component:
//   import recipes from '../../data/recipes.json';
// Keeping it server-side keeps prompt text out of the client bundle. That is a
// product decision, not a technical one — relax it if the team decides prompts are
// public works.

export type Recipe = {
  id: string;
  title: string;
  summary: string;
  sourcePostUrl: string;
  /** null until someone verifies the Threads post. Render "來源待確認", never a guess. */
  creatorName: string | null;
  creatorInstagramUrl: string | null;
  /** Original prompt text, verbatim. Never sent from the browser to /api/generate. */
  prompt: string;
  inputNote: string;
};
