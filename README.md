# A gift for generations

A land gift and partnership invitation for **82 Claytons Road, Amity, Minjerribah / North Stradbroke Island**, prepared by **Luke Nathan Hayes** for Anglican Church Southern Queensland.

**[Visit the public website](https://auraofintelligence.github.io/Anglican-Diocese-82-Claytons-Amity/)** · **[Read the 11-page proposal](https://auraofintelligence.github.io/Anglican-Diocese-82-Claytons-Amity/documents/82-Claytons-Road-Anglican-Partnership-Proposal.pdf)** · **[Explore the document library](https://auraofintelligence.github.io/Anglican-Diocese-82-Claytons-Amity/documents.html)**

The invitation connects dementia support, aged care and longevity research with Aura Geode, Aura Genesis, a proposed Straddie Sovereign Wealth Fund, C-hours, learning and community participation. Joyful Responsible Abundance provides the wider human purpose.

## Website

The eleven proposal pages preserve the approved manuscript word for word. Additional pages provide a searchable library of all 31 supplied documents, links to other Minjerribah proposals, and the Strange But True licence. The PDF references page links back to the website.

The site includes eleven distinct full-width GenAI heroes, contextual future-technology images, vertical tower gardens, a GenAI favicon, original supplied property maps, linked references, previous/next navigation, a floating back-to-top button, and pointer/touch-responsive cards. Reduced-motion preferences are respected.

82 Claytons Road is landlocked, beside Claytons Road. Property-related concept artwork uses a wooded setting without ocean or bay views. The globe illustration expresses the wider international vision. All generated artwork is labelled as concept imagery, and does not depict an approved design or existing facility.

## Source documents

`content/proposal.md` is the approved manuscript, including the requested website notice. `content/documents.json` lists the original supplied files with SHA-256 checksums. Their original bytes are preserved. These background documents trace the development of the ideas; the proposal states the current invitation, including a C-hour model without monetary equivalence.

The supplied property map screenshots were brought across from the existing Minjerribah site with their original Google Maps attribution. The original property PDF is available in the document library. Other referenced organisations and research remain linked to their original sources.

## Maintain the site

This is a static, dependency-free website. No account, tracking, database or server is required for visitors. Google Fonts is used for typography, with system fallbacks.

With Python installed:

```text
python scripts/build.py
python scripts/check.py
python -m http.server 4173
```

The checker verifies the eleven proposal sections against the manuscript, original document hashes, local links, reference anchors and image paths. Commit the generated HTML together with the source changes. GitHub Pages serves the `main` branch from the repository root.

Original artwork was created with the built-in image-generation tool. The final prompt set is recorded in [`content/image-prompts.json`](content/image-prompts.json); web assets are in [`assets/images/`](assets/images/).

## Licence

[Strange But True Public Source Licence](LICENCE.md). Original work by Luke Nathan Hayes / Strange But True / Aura of Intelligence. This is a public source licence, not an open-source licence. Third-party material retains its own rights and attribution.

Contact: [auraofintelligence@gmail.com](mailto:auraofintelligence@gmail.com)
