# Contact form — what's done and what's left

_Re: Aquaboss memo, 6-17-26. Written for a first-timer — no jargon assumed._

## What I built (done, live in the site)

- **`get-involved.html`** — the single Get Involved page now holds both the "ways to help" cards and the full contact form from the spec:
  - Required: full name, email, "What are you reaching out about?", message.
  - Optional: organization, role/title, website/LinkedIn, "How would you like to help?" checkboxes.
  - Two lane chips at the top ("Support Pergamon" / "Get Involved") that set the category.
  - Conditional fields that appear only when relevant (support type + level for donors; expertise + availability for collaborators).
  - Required consent checkbox.
  - Inline validation with clear error messages, and an on-page success message.
  - Built-in basic spam protection (a hidden "honeypot" field) plus a ready slot for Cloudflare Turnstile.
  - Fully responsive and keyboard/screen-reader accessible.
- Merged the old separate Contact page into Get Involved (one page, no duplication); Support buttons jump straight to the form (`get-involved.html#form`).
- Set the contact email to `support@projectpergamon.ai`.

## The ONE code step left (someone has to paste a value)

The form is wired to send submissions to a single web address that doesn't exist yet. Right now it runs in **preview mode**: it validates and shows the thank-you message, but does **not** deliver anything. Open `get-involved.html`, find this line near the bottom, and paste your endpoint between the quotes:

```js
const FORM_ENDPOINT = "";
```

The easiest endpoint for a beginner is **Formspree** (formspree.io): make a free form, copy the URL it gives you, paste it in. That alone gets submissions emailed to you. To also log into Airtable, point the form at a small handler (Formspree + a Zapier/Make automation, or a Cloudflare/Netlify function) — but email first is fine for v1.

## The non-code setup (accounts + purchases — I can't do these for you)

These all require logging into accounts, paying, or owning a domain, so they're yours (or the bot's) to do. Order matters:

1. **Buy the domain** `projectpergamon.ai` — Namecheap, Porkbun, or Cloudflare Registrar.
2. **Set up Google Workspace** on that domain and create `support@projectpergamon.ai`.
3. **Verify the domain + add MX, SPF, DKIM, DMARC records** — Google gives you the exact values to copy-paste into the registrar's DNS dashboard.
4. **Create the Airtable base** — table "Inbound Inquiries" with the fields listed in the memo.
5. **Get a Cloudflare Turnstile site key** (free), paste it into the `data-sitekey` slot on the `cf-turnstile` div in `get-involved.html`, un-hide it, and add the Turnstile `<script>` tag to the page `<head>`.
6. **Connect the form** by filling in `FORM_ENDPOINT` (step above) so submissions email `support@` and create an Airtable record.

Until 1–3 are done, the form still works in preview mode — you just can't receive mail at the custom address yet. None of this requires understanding DNS deeply; it's mostly copy-paste.
