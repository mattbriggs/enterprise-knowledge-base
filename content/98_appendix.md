---
title: "Appendices"
slug: 98_appendix
---

# 4. Appendices  

### 4.1 Glossary of Terms  
*(This glossary defines terms and domain-specific language used in the SRS to ensure clarity.)*

- **Atomic Container / Content Item:** A discrete unit of content managed by GKCMS, which includes both the content data (text, etc.) and associated metadata. Called "atomic' to imply it's a smallest standalone piece (like an article, a FAQ entry, etc.).  
- **Author-First Workflow:** A content creation approach where a human author uses the system's interface to create content from scratch (as opposed to content being primarily ingested or generated elsewhere).  
- **Headless CMS:** A content management system that provides content via API (decoupled from presentation). GKCMS acts as a headless CMS by allowing content to be created and then delivered through APIs to any front-end (like a static site or an app).  
- **Schema:** The structure or blueprint for a content type. Schemas define what fields a content item of that type must/may have (for example, a "NewsArticle' schema might include fields: headline, body, author, publishDate).  
- **Field:** An individual piece of data within a content item, defined by the schema. Fields have types (text, date, reference, etc.), and possibly constraints (like max length, required).  
- **Syntax Definition:** Rules or patterns for content formatting. In GKCMS context, this could refer to templates for text (like predefined Markdown snippets or allowed HTML tags). It might also relate to any domain-specific markup.  
- **Validation Rule:** A conditional constraint on content beyond the basic schema. For example, "if content type is X, field Y must be in the past'. Or "the combination of fields A and B must be unique across all items'.  
- **Data Dictionary:** A curated set of definitions for data elements or terms. It serves as a reference such that if multiple schemas have a "Customer ID' field, the data dictionary would have one entry explaining what "Customer ID' means, its format, etc. In GKCMS, it also can serve as a glossary for terms. A business glossary is similar, but often data dictionary is more for technical fields. We have a hybrid usage here [oai_citation:33‡thedatamaven.net](https://thedatamaven.net/2017/04/whats-the-difference-glossary-dictionary-taxonomy-ontology/#:~:text=A%20Data%20Dictionary%20is%20an,will%C2%A0include%20semantic%20name%20and%20definition).  
- **Terminology / Glossary Terms:** The controlled list of terms (vocabulary) relevant to the content. For instance, in a medical knowledge base, terms might include diseases, symptoms, treatments. Each term often has a definition (which might be stored in data dictionary or separately) [oai_citation:34‡thedatamaven.net](https://thedatamaven.net/2017/04/whats-the-difference-glossary-dictionary-taxonomy-ontology/#:~:text=What%20is%20a%20glossary%3F) [oai_citation:35‡thedatamaven.net](https://thedatamaven.net/2017/04/whats-the-difference-glossary-dictionary-taxonomy-ontology/#:~:text=What%20is%20a%20dictionary%3F).  
- **Ontology:** A formal representation of knowledge as a set of concepts (terms) within a domain, and the relationships between those concepts. In GKCMS, the ontology primarily provides a hierarchy (taxonomy) of terms (category/subcategory relationships) and possibly other link types (like "is related to'). It helps organize content semantically (e.g. knowing that "Hypertension' is a type of "Cardiovascular disease' helps group content).  
- **Knowledge Graph:** A network (graph) of entities (like content items, terms, authors, etc.) linked by relationships that convey meaning (like "authored by', "mentions', "belongs to category'). It's the backbone for advanced querying (like find content related via certain terms) and for providing context to AI/search algorithms [oai_citation:36‡yext.com](https://www.yext.com/platform/content#:~:text=).  
- **JSON-LD:** A JSON-based format to serialize linked data (i.e., data that references a context or vocabulary, enabling it to be linked across systems). It's embedded in HTML to help search engines (and other agents) understand the structure of the information on the page. GKCMS uses JSON-LD to expose the knowledge graph data of content on the static site, aligning with schema.org or custom vocabularies for semantic SEO [oai_citation:37‡yext.com](https://www.yext.com/platform/content#:~:text=).  
- **Embedding (Vector):** A numeric vector that represents semantic aspects of content. Two content items with similar topics will have embeddings that are close in the vector space (as measured by cosine similarity or Euclidean distance). We use embeddings for semantic search.  
- **Weaviate:** An open-source vector database that also incorporates a schema and can perform hybrid queries (keyword + vector). Notably, Weaviate can be seen as an "AI-native' database [oai_citation:38‡azumo.com](https://azumo.com/software-developer/weaviate#:~:text=Hire%20Nearshore%20Weaviate%20Developers%20,search%20and%20knowledge%20graph%20exploration). In GKCMS, used to store content vectors and allow similarity queries.  
- **Neo4j:** A graph database management system. Used in GKCMS to store the knowledge graph (content and ontology relations).  
- **FastAPI:** A modern Python web framework used to build the GKCMS API. Chosen for performance (asynchronous support) and concise code with automatic docs.  
- **OAuth 2.0 / OIDC:** Authentication framework/protocol. GKCMS leverages this for login and token issuance, delegating identity management to a provider. OIDC (OpenID Connect) is an extension on top for getting user info.  
- **RBAC:** Role-Based Access Control. In GKCMS, roles like "admin', "editor', "reader' define what actions a user (or token bearer) can perform.  
- **Prometheus:** A monitoring system and time-series database. GKCMS exposes metrics in a format Prometheus can scrape to collect performance data.  
- **Mermaid Diagrams:** Not part of the system per se, but a tool we used in documentation (like this SRS) to describe graphs and diagrams in text form.  

### 4.2 Acronyms and Abbreviations  

- **GKCMS:** Generic Knowledge & Content Management Platform (the system being specified).  
- **CMS:** Content Management System. Software for creating, managing, and delivering digital content.  
- **IEEE:** Institute of Electrical and Electronics Engineers. (IEEE 830 is a standards document for SRS format).  
- **YAML:** "YAML Ain't Markup Language' - a human-readable data serialization format (often used for configuration or front matter). Used in GKCMS for structured content data.  
- **JSON:** JavaScript Object Notation - a lightweight data-interchange format. Used for APIs and storage (some content and metadata).  
- **JSON-LD:** JSON for Linked Data. Used to embed semantic context in web pages [oai_citation:39‡yext.com](https://www.yext.com/platform/content#:~:text=).  
- **UI:** User Interface.  
- **API:** Application Programming Interface. Here typically refers to web service endpoints of GKCMS.  
- **CRUD:** Create, Read, Update, Delete - the four basic functions of persistent storage.  
- **NLP:** Natural Language Processing. Implied in context of entity tagging or embedding (the system might use NLP models for those).  
- **SEO:** Search Engine Optimization. The practice of making content more discoverable by search engines - JSON-LD contributes to this.  
- **IdP:** Identity Provider (in context of OAuth2, the external service that authenticates users and issues tokens).  
- **JWT:** JSON Web Token - a type of token often used in OAuth2 to represent user's authenticated session, containing claims.  
- **ASVS:** Application Security Verification Standard (by OWASP). We target Level 2 of ASVS [oai_citation:40‡versprite.com](https://versprite.com/blog/software-development-life-cycle/#:~:text=Level%201%20%E2%80%93%20First%20step%2C,verify%20with%20black%20box%20testing).  
- **OWASP:** Open Web Application Security Project - an organization that provides security guidelines.  
- **XSS:** Cross-Site Scripting, a web security vulnerability where malicious scripts are injected into content.  
- **CSRF:** Cross-Site Request Forgery (not specifically mentioned above, but typically considered - likely mitigated by using OAuth2 tokens and same-site cookies as relevant).  
- **CI/CD:** Continuous Integration / Continuous Deployment, referring to automated build and test processes (implied under testability/maintainability).  
- **PoC:** Proof of Concept. A preliminary version to demonstrate feasibility.  
- **SLA:** Service Level Agreement - a contract (or commitment) for performance levels (uptime, etc.) [oai_citation:41‡radview.com](https://www.radview.com/blog/in-the-spotlight-the-sla-for-performance-and-load-testing/#:~:text=Performance%20Testing%20%20has%20become,in%20Performance%20and%20Load%20Testing).  
- **KPI:** Key Performance Indicator - a measurable value to evaluate success in meeting objectives [oai_citation:42‡bmc.com](https://www.bmc.com/blogs/sla-vs-kpi/#:~:text=Both%20the%20Service%20Level%20metrics,regarded%20as%20an%20SLA%20term). In GKCMS context: metrics like response time, throughput, etc., that reflect system health/performance.  
- **CDN:** Content Delivery Network - used to serve static site files globally with low latency.  
- **SQL/NoSQL:** Types of database. Not explicitly mentioned in text, but Document Store could be a NoSQL and we have Neo4j (graph DB) which is non-relational.  
- **HTTP/HTTPS:** Hypertext Transfer Protocol (Secure). The protocol for data communication for the web and API.  
- **HTML:** Hypertext Markup Language - format of web pages generated for static site.  
- **URL:** Uniform Resource Locator - addresses for API endpoints, etc.  
- **SPA:** Single Page Application - not necessarily what static site is (likely static site is multi-page static), but admin UI might be an SPA if implemented.  
- **GIL:** Global Interpreter Lock (Python-specific, a constraint for concurrency).  

*End of System Requirements Specification.* 

**References:** (Citations as listed inline, e.g., [oai_citation:43‡chrisdaaz.github.io](https://chrisdaaz.github.io/static-web-scholcomm/tutorials/static-site-generators/#:~:text=YAML%20syntax%20is%20strict%3B%20invalid,an%20error%20you%20don%E2%80%99t%20understand) correspond to the sources in section 1.4)