# TAsAutomation

-- keep in mind this is just a prototype to test functionality --

main file is TAsAutomation.py

This tool uses a predefined list of RSS feeds to ingest recent Cybersecurity topics, events, and most importantly... vulnerabilities. It uses a SQLLite database for easy deployment as it is meant to be run in just a local machine. This database contains the raw content and the cleaned/sanitized content for the LLM to ingest. It also contains the calculated raw_content hash to check for dupes in case some news feeds have the same article.

The cleaned content should be character limited for the LLM to ingest as well as token limited since local LLMs are limited to their hardware.

Each source is also treated equally as there is a minimum number of articles grabbed PER source for variety.

Processed articles (articles that have been analyzed AND sent) are marked and make room for new articles to be published. The response from the LLM is then formatted into a proper email and sent.

-- WHAT YOU NEED TO DO FOR RUNNING IT IN YOUR LOCAL INSTANCE (FULL CAPABILITIES) --

* Launch your own local LLM instance, I use LM Studio and have it run w/ ur preferred model.
* Tailor the email list, local llm / api key (if cloud), email sending function (secrets.py), to your needs.




-- THINGS TO BE ADDED / IMPROVED --

* config files for easier deployment, security, and scalability
* multiple llm agents can be used, like one for summarization to shorten char length for ingesting and processing, the next for deeper insights and mitigations
* vector database for RAG models if we move from specific rulesets to further insight (though this is more for users wanting to deeply conversate with LLMs provided the data)
* email propagation is kinda crude rn, could have a predefined list of subject headers to be more dynamic/interesting AND when scaling up, trusted email domains + mail servers should be used if we want newsletter to reach every inbox (currently this has a high chance of being automatically marked as spam)

