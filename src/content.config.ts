import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const research = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/research" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    // Short note under the title (coauthors, venue, status)
    note: z.string().optional(),
    abstract: z.string().optional(),
    keywords: z.array(z.string()).default([]),
    conclusions: z.array(z.string()).default([]),
    // Materials: papers, slides, external code links
    materials: z
      .array(z.object({ label: z.string(), href: z.string() }))
      .default([]),
    // Languages/packages used in the code
    packages: z.array(z.string()).default([]),
    // URL to open the notebook in Google Colab
    colab: z.string().url().optional(),
    // Site-relative path to the downloadable .ipynb (in public/)
    notebook: z.string().optional(),
    // Site-relative path to the embedded marimo app (in public/)
    app: z.string().optional(),
    appHeight: z.number().default(780),
  }),
});

const teaching = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/teaching" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    semester: z.string(),
    professor: z.string().optional(),
    institution: z.string().default("University of Costa Rica"),
  }),
});

export const collections = { research, teaching };
