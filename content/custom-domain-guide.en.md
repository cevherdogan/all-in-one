---
title: "Setting up a Custom Domain on GitHub Pages via Hostinger"
description: "Step-by-step guide for mapping all-in-one.foundral.tech to a GitHub Pages site."
badges: [Guide, GitHub Pages, DNS]
slug: "custom-domain-guide"
lang: "en"
---

This guide walks you through connecting a **Hostinger-managed domain** to a **GitHub Pages** site, using the example `all-in-one.foundral.tech`.

## 1. Prerequisites
- A GitHub Pages-enabled repository:  
  Example: https://github.com/cevherdogan/all-in-one  
  Default Pages URL: https://cevherdogan.github.io/all-in-one/
- Access to Hostinger’s **hPanel** for `foundral.tech`.

## 2. Add a CNAME Record in Hostinger
1. Log into Hostinger: [DNS Zone Editor](https://hpanel.hostinger.com/domain/foundral.tech/dns)
2. Click **Add New Record**.
3. Fill in:
   ```
   Type: CNAME
   Name: all-in-one   (without @)
   Target: cevherdogan.github.io
   TTL: 3600
   ```
4. Save changes.

## 3. Configure GitHub Pages
1. Go to your repo’s **Settings → Pages**.  
2. In **Custom domain**, enter:
   ```
   all-in-one.foundral.tech
   ```
3. Check **Enforce HTTPS** (enable after DNS resolves).

## 4. Wait for DNS Propagation
- This can take 15 minutes to 24 hours.
- Verify with:  
  ```
  nslookup all-in-one.foundral.tech
  ```
  or online tools like [whatsmydns.net](https://www.whatsmydns.net/).

## 5. Confirm Your Site is Live
Once DNS resolves and HTTPS is enforced, your site will be live at:  
**https://all-in-one.foundral.tech/**

## ✅ Example Deployment Log
> “Your site is live at https://all-in-one.foundral.tech/  
> Last deployed by @cevherdogan — 13 minutes ago”

## Community Learning
This process is now documented for all contributors to:
- Learn domain mapping basics
- Replicate for their own projects
- Contribute localized translations of this guide
