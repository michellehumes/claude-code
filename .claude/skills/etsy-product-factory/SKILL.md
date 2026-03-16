# etsy-product-factory

## Execution Environment

The etsy-product-factory skill must determine the correct execution environment for every task.

There are two environments:

1. Local Mac environment
2. Claude Code browser environment (Chrome)

---

## Core Rule

Any task that requires internet access, websites, or browser automation must be executed by Claude Code using its Chrome environment.

Claude Code should be considered the default executor for all online workflows.

---

## Browser Execution Tasks (Claude Code)

Claude Code must execute any workflow that requires interaction with the internet or a web interface.

This includes but is not limited to:

* accessing Etsy.com
* creating Etsy listings
* editing Etsy listings
* uploading listing images
* filling listing attributes
* entering titles, descriptions, and tags
* interacting with dashboards
* scraping market data
* running Playwright automation
* browser automation
* interacting with any SaaS tools
* verifying published listings
* checking listing performance pages

Claude Code should use its Chrome environment whenever these tasks occur.

If a workflow step involves a website, the task must automatically route to Claude Code.

---

## Local Execution Tasks (Mac)

Local execution should only be used for tasks that do not require internet access.

Examples include:

* generating image prompts
* writing product titles and descriptions
* generating Etsy SEO keywords
* creating listing copy
* generating digital download templates
* creating spreadsheet tools
* preparing product assets
* organizing local files
* generating prompt libraries
* preparing listing image instructions

These tasks may run locally because they involve text or file preparation only.

---

## Hybrid Workflows

Many Etsy workflows require both local preparation and browser execution.

The correct order is:

1. Generate assets locally
2. Prepare listing data locally
3. Generate prompts, titles, descriptions, and tags
4. Prepare images or files
5. Then route execution to Claude Code to complete the online steps.

Claude Code must then:

* open Etsy
* create the listing
* upload images
* populate all listing fields
* publish or save the listing

---

## Default Behavior

The etsy-product-factory skill must default to Claude Code execution whenever a task touches the internet or a website.

If there is uncertainty about where a task should run, prefer the Claude Code browser environment.

---

## Automation Priority

The goal of this skill is to enable automated Etsy product creation pipelines.

Claude Code should be used to automate the following whenever possible:

* listing creation
* listing updates
* listing publishing
* image uploads
* attribute entry
* SEO tag entry
* listing verification

This ensures the skill can run end-to-end Etsy workflows without manual browser interaction.
