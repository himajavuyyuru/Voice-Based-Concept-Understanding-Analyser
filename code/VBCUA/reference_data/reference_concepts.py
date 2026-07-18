"""
Predefined reference concept explanations.
Each entry contains a canonical explanation of the concept that user
speech will be semantically compared against.
"""

REFERENCE_CONCEPTS = {
    "Machine Learning": (
        "Machine learning is a branch of artificial intelligence where "
        "computer systems learn patterns from data instead of being "
        "explicitly programmed. Algorithms are trained on datasets to "
        "make predictions or decisions, and the model improves its "
        "performance as it is exposed to more data. Common types include "
        "supervised learning, unsupervised learning, and reinforcement "
        "learning."
    ),
    "Cloud Computing": (
        "Cloud computing is the delivery of computing services such as "
        "servers, storage, databases, networking, and software over the "
        "internet, commonly called the cloud. It allows organizations to "
        "access resources on demand without owning physical hardware, "
        "offering scalability, flexibility, and pay-as-you-go pricing. "
        "Major service models include IaaS, PaaS, and SaaS."
    ),
    "Artificial Intelligence": (
        "Artificial intelligence refers to the simulation of human "
        "intelligence in machines that are programmed to think, reason, "
        "and learn. It encompasses areas such as machine learning, "
        "natural language processing, computer vision, and robotics, "
        "enabling systems to perform tasks that typically require human "
        "cognition."
    ),
    "Data Structures": (
        "Data structures are specialized formats for organizing, "
        "processing, retrieving, and storing data efficiently. Common "
        "examples include arrays, linked lists, stacks, queues, trees, "
        "and graphs. Choosing the right data structure improves the "
        "efficiency of algorithms in terms of time and space complexity."
    ),
    "Computer Networks": (
        "A computer network is a collection of interconnected devices "
        "that communicate and share resources using a set of communication "
        "protocols. Networks can be classified as LAN, WAN, or MAN based "
        "on their geographical scope, and they rely on components such as "
        "routers, switches, and the TCP/IP protocol suite to transmit "
        "data reliably."
    ),
}


def get_concept_names():
    return list(REFERENCE_CONCEPTS.keys())


def get_reference_text(concept_name: str) -> str:
    return REFERENCE_CONCEPTS.get(concept_name, "")
