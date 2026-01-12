---
hide:
  - navigation
  - toc
---
<style>
. md-content {
    max-width: 100%;
}
. md-content__inner {
    margin: 0 auto;
}
h1:first-of-type {
    display: none;
}
.hero {
    text-align: center;
    padding: 2rem 1rem 4rem 1rem;
}
.hero.banner {
    max-width: 900px;
    width: 100%;
    margin-bottom: 2rem;
}
.hero p {
    font-size: 1.1rem;
    opacity: 0.8;
    margin-bottom: 1rem;
}
.buttons {
    display: flex;
    gap: 1rem;
    justify-content:  center;
    flex-wrap:  wrap;
    margin-top:  2rem;
}
. button-primary, .button-secondary {
    padding: 0.8rem 2rem;
    border-radius: 0.3rem;
    text-decoration:  none;
    font-weight:  600;
    transition: transform 0.2s;
    display: inline-block;
}
.button-primary {
    background: var(--md-primary-fg-color);
    color: var(--md-primary-bg-color);
}
.button-secondary {
    border:  2px solid var(--md-primary-fg-color);
    color: var(--md-primary-fg-color);
}
.button-primary:hover, .button-secondary:hover {
    transform: translateY(-2px);
}
.section {
    padding: 3rem 1rem;
    max-width:  1200px;
    margin: 0 auto;
}
.section-title {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom:  3rem;
    font-weight: 700;
}
</style>

<div class="hero" markdown>

<!-- PROJECT LOGO -->
<img src="assets/images/logo-banner.png" class="banner" style="width:35vw">


[![CI](https://github.com/luisfabib/fhircraft/actions/workflows/CI.yaml/badge.svg?branch=main&event=push)](https://github.com/luisfabib/fhircraft/actions/workflows/CI.yaml?style=flat&labelColor=%231e293b)
![PyPI - Version](https://img.shields.io/pypi/v/fhircraft?labelColor=%231e293b&logo=python&label=Release)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
![FHIR Releases](https://img.shields.io/badge/FHIR-R4_R4B_R5-blue?style=flat&logo=fireship&logoColor=red&labelColor=%231e293b)


*Pythonic FHIR development with type safety and modern tooling*


[Get Started :fontawesome-solid-rocket:](quickstart/quickstart.md){ .md-button .md-button--primary }

</div>


!!! warning "Active development"
  
    This package is under active development. Breaking changes can occur in future pre-releases.

---

<div class="section" markdown>

## :material-star-outline: Why Choose Fhircraft? 

<div class="grid cards" markdown>

-   :material-shield-check-outline:{ .lg .middle } **Type Safety & Validation**

    ---

    Generate validated Pydantic models from FHIR specifications. Catch data errors at development time, not in production.

-   :material-language-python:{ .lg .middle } **Pythonic FHIR Development**

    ---

    Work with FHIR resources using familiar Python patterns. No need to learn complex FHIR server infrastructure. 

-   :material-package-variant-closed:{ .lg .middle } **Multi-Release Support**

    ---

    Seamlessly work with FHIR R4, R4B, and R5. Switch between versions as your project requires. 

-   :material-file-search-outline:{ .lg .middle } **FHIRPath Integration**

    ---

    Query and validate FHIR data using the standard FHIRPath language, fully integrated with Python.

-   :material-cog-outline:{ .lg .middle } **Flexible Architecture**

    ---

    Use local files for security, remote URLs for convenience, or hybrid approaches for production systems.

-   :material-swap-horizontal:{ .lg .middle } **Mapping Integration**

    ---

    Leverage the FHIR Mapping Language to define conversions between FHIR resources, fully integrated with Python. 

</div>

</div>

---

<div class="section" markdown>

## :material-cloud-download-outline: Installation

=== ":simple-pypi: pip"

    ```bash
    pip install fhircraft
    ```

=== ":simple-poetry: Poetry"

    ```bash
    poetry add fhircraft
    ```

=== ":material-lightning-bolt: uv"

    ```bash
    uv add fhircraft
    ```

=== ":octicons-package-16: pipenv"

    ```bash
    pipenv install fhircraft
    ```

For further information see the [Installation Guide](quickstart/installation.md).


</div>

---

<div class="section" markdown>

## :material-lightning-bolt:{ .lg } Key Capabilities

<div class="grid" markdown>

!!! success "Pydantic Models"
    Auto-generated, type-safe models for all FHIR resources.  Full IDE autocomplete and validation support.

!!! info "FHIRPath Queries"
    Execute FHIRPath expressions directly on your resources. Standard-compliant querying made simple.

!!! tip "Version Flexibility"
    Work across FHIR versions without rewriting code. Future-proof your healthcare applications.

!!! abstract "Resource Mapping"
    Transform between different FHIR resource types using the official Mapping Language specification. 

</div>

</div>

---

<div class="section" style="text-align: center; padding-bottom: 4rem;" markdown>

## Ready to Build with FHIR?

<div class="buttons">
    <a href="user-guide/" class="button-primary">Read the Guide</a>
    <a href="api-reference/" class="button-secondary">API Reference</a>
    <a href="https://github.com/luisfabib/fhircraft" class="button-secondary">: material-github: GitHub</a>
</div>

</div>