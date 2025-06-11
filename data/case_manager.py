"""
Case management system - handles different detective cases and their documents
"""
from typing import List
from utils.document_system import DocumentDiscoverySystem, RAGSystem, Document


class CaseDocumentManager:
    """Manages documents for a specific case"""

    def __init__(self, case_name: str):
        self.case_name = case_name
        self.discovery_system = DocumentDiscoverySystem()
        self.rag_system = RAGSystem()
        self.setup_case_documents()

    def setup_case_documents(self):
        """Setup documents for the current case"""
        if self.case_name == "seaside_cottage": # formerly mystery_mansion
            self._setup_cottage_documents()
        elif self.case_name == "art_theft":
            self._setup_corporate_documents()
        # Add more cases here as you expand

    def _setup_cottage_documents(self):
        """Setup documents for the Seaside Cottage case"""
        documents = [
            Document(
                id="guest_list",
                title="Guests Marco Remembers from Last Night",
                content="""Guests present: Marco Constantino (myself), 
                         Charles Rigby (that's you),
                         Lady Agatha Grimsby, Dr Pike (Horace),
                         Clara Pike, Eliot and Maeve Grimsby, and Ms Delilah Snipe. 
                         I remember they stayed until after midnight, when I went to sleep.
                    """,
                keywords=["guests", "guest list", "who was there", "visitors", "people", "attendees"],
                category="records",
                importance=3,
                discovery_message="You found out who was at the cottage last night!"
            ),
            Document(
                id="agatha_interview",
                title="Our First Interview with Lady Agatha",
                content="""What did you do today?
                        Well, I suppose the towngoing party departed at about quarter to 7 - a little tardy.
                        We stopped for breakfast with my friend Beatrice - another of the poor girls husbands died, poor thing.
                        Horace left partway through to get a fresh fish for a dinner bake from the fishmonger,
                        I daresay quite rude to leave us, at about quarter of 10.
                        After breakfast Delilah and I stopped at the gardeners' for an impromptu arrangement. We returned to the cottage a hair past 12...
                        ... and interrupted my meal in the garden ...
                        No, Marco, I daresay wet cheese a tomato and bucket of wine do not constitute a meal...
                        ... dio sancto, non sai cosa stai dicendo! ...
                        Hmpf! Well, you know the rest.
                        Yes Mrs Grimsby, I know the rest. Thank you. 
                    """,
                keywords=["Agatha", "town", "brunch", "Lady Agatha", "Mrs Grimsby", "going to town", "Agatha Grimsby"],
                category="witness_statement",
                importance=2,
                discovery_message="We didn't learn much from Lady Agatha..."
            ),
            Document(
                id = "agatha_followup_1",
                title = "Our Next Question for Lady Agatha",
                content = """ 
                        Apologies for interrogating you again miss, but when you were leaving to go into the town, 
                        did you see who delivered the milk? With the note with the H?
                        No, it wasn't on the step when we left. But we saw Hugo's cart on the road.
                        He doesn't work for us anymore - but he's still handy - such a kind man.
                        Hm, ok, thank you.
                    """,
                keywords = ["milk", "road", "cart", "Hugo", "groundskeeper", "butler", "kitchen"],
                category = "witness_statement",
                importance = 4,
                discovery_message = "There may be an unfamiliar face to consider..."
            ),
            Document(
                id="maeve_interview",
                title="Our First Interview with Maeve Grimsby",
                content=""" You've had such a busy day eh? Tell me about it, please. Indeed, well, Eliot and I left the cottage around 5, quite early.
                    We reached town before 6, and went with Captain Griggs to resupply the lighthouse.
                    And these supplies, what were they?
                    Mostly whiskey, awful quality. Potatoes, bread, I'd imagine those are the typical stoic rations.
                    Inhumane! Please do continue.
                    Yes, well we got close to the seamount the lighthouse is on, circled around looking for a safe place to pull in,
                    but...
                    But?
                    But there just wasn't and the fog was coming in fast, so we left.
                    Or at least that's what Griggs said, but he'd had a little much of that swill for my taste.
                    And you returned to the cottage at around 11, yes?
                    Of course, you remember we smoked in the garden.
                    Sh! Lady Agatha may be able to hear us through the door! Thank you.
                """,
                keywords=["sailing", "maeve", "eliot", "daughters", "lighthouse", "art"],
                category="witness_statement",
                importance=3,
                discovery_message="We learn about the failed sailing trip..."
            ),
            Document(
                id="maeve_followup_1",
                title="We have more Questions for Maeve...",
                content="""
                    And Maeve, did yourself or Eliot see anybody on the road when you were going down to the docks?
                    No - 
                    Just curious - and did you on your way back?
                    ... No, why?
                    I am just checking. And you were with him the entire time, yes?
                    Yes, until I went to the beach with Clara…
                    Our victim?
                    Yes...
                    And you did not share this before why?!
                    ...please I was so scared…
                    Silly girl! And when did she leave you on the beach?
                    We came back together I swear! 
                    A likely story! And who maybe saw you together then, hm?
                    Maybe Delilah? We saw someone looking out from a window when we were on the footpath.
                    Hmpf! Alright, stay in the study please. We will step away a moment.
                """,
                keywords=["beach", "milk", "road", "cart", "window", "upstairs", "with Clara"],
                category="witness_statement",
                importance=5,
                discovery_message="Maeve might have been the last person with Clara!"
            ),
            Document(
                id="griggs_interview",
                title="We interview Captain Griggs",
                content=""" 
                    Buongiorno, Capitano. The air is thick today — but not as thick as the tales you are said to tell.
                    You here to ask about the sea, or about the girl?
                    Both. Let us begin with the easier. You left this morning, si?
                    At first light. Took the Grimsby lad and his lass down the coast. The lighthouse run.
                    A noble voyage. But... you returned early, yes?
                    The fog rolled in like a drunk uncle. Couldn’t see ten feet. I turned the boat around at half past ten.
                    Hmm. And you left them where?
                    Dropped 'em just where I picked 'em. Back at the dock. Eliot was barking. Maeve — quiet as ever.
                    And then?
                    I came back here to town. Nipped into the pub with ol' Hugo for a pint. Better than tea.
                    Alright, I'll be off. Thank you for your time, Capitano.
                """,
                keywords=["captain griggs", "the captain", "griggs"],
                category="records",
                importance=2,
                discovery_message="We don't learn much from Captain Griggs..."
            ),
            Document(
                id="delilahs_notes",
                title="Delilah’s Annotated Book Page",
                content="""
                    Found in Delilah’s room, on her bed. A page corner was folded and faint writing seen in the margin:
                    'The killer came when the fog was thickest... and he used the sword that was never meant to be seen again.'
                    Below this: a hand-written note — 'Griggs would never... but Eliot, perhaps? No...'
                    The underlined passage is from Chapter 12 of 'Blood on the Brambles.'
                """,
                keywords=["Delilah", "book", "fog", "Eliot", "Griggs", "notes"],
                category="literature_note",
                importance=2,
                discovery_message="We found a note in Delilah's mystery novel — seems like she's on edge..."
            ),
            Document(
                id="cleaning_receipt",
                title="Signed Supply Receipt",
                content="""
                    Dated the day before the murder. 
                    'To: Garden Cottage Estate, per standing order. Received by: H. — 1 crate bleach, 1 brush, 2 pairs gloves, 1 soapstone scrub.'
                    The signature 'H.' is scrawled in black ink.
                    No one on record has this as an initial — except perhaps Hugo, the former groundskeeper.
                """,
                keywords=["receipt", "cleaning supplies", "signature", "evidence", "H."],
                category="forensic_clue",
                importance=4,
                discovery_message="A receipt signed 'H.', but nobody says he works here...."
            ),
            Document(
                id="footprint_report",
                title="Footprint Found in Attic",
                content="""
                    An initial sketch made by Marco before the scene was disturbed:
                    'Single footprint. Men's size ~10.5, work boot. Slight taper on the right heel.
                    Not consistent with Eliot (size 8) or Dr. Pike (size 12).
                    Footprint was near the trunk and sword stand.
                    Later, footprint seems smudged — possibly tampered with.
                    The dust pattern suggests someone tried to obscure it post-facto.'
                """,
                keywords=["attic", "footprint", "dust", "size", "shoe", "tampered", "work boot"],
                category="forensic_clue",
                importance=4,
                discovery_message="Before it was tampered with, Marco sketched a footprint from the attic. It doesn’t match anybody present...."
            ),

        ]

        # Add documents to discovery system
        for doc in documents:
            self.discovery_system.add_document(doc)

    # Incomplete - art heist not implemented yet
    def _setup_corporate_documents(self):
        """Setup documents for a corporate theft case (example for expansion)"""
        # This is where you'd add documents for other cases
        documents = [
            Document(
                id="employee_records",
                title="Recent Employee Activity",
                content="Unusual after-hours access detected for several employees last week...",
                keywords=["employees", "staff", "access", "after hours"],
                category="records",
                importance=3,
                discovery_message="Employee records show suspicious activity!"
            )
        ]

        for doc in documents:
            self.discovery_system.add_document(doc)

    def process_input(self, text: str) -> tuple:
        """Process user/AI input for document discovery and RAG context"""
        # Check for new document discoveries
        newly_discovered = self.discovery_system.check_for_discoveries(text)

        # Add newly discovered documents to RAG system
        if newly_discovered:
            self.rag_system.add_documents(newly_discovered)

        # Get RAG context for current input
        rag_context = self.rag_system.create_context_for_prompt(text)

        return newly_discovered, rag_context

    def get_discovered_documents(self) -> List[Document]:
        """Get all discovered documents"""
        return self.discovery_system.get_discovered_documents()

    def get_case_summary(self) -> str:
        """Get a summary of discovered clues"""
        discovered = self.get_discovered_documents()
        if not discovered:
            return "No clues discovered yet."

        summary = f"DISCOVERED CLUES ({len(discovered)}):\n"
        for doc in discovered:
            summary += f"• {doc.title} ({doc.category})\n"

        return summary