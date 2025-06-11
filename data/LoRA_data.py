# I am well aware that this is a small and ineffeciently organized dataset, but it's good enough for now.
examples = [
    {"text": "Q: What did Lady Agatha think of the local tea?\nA: Lady Agatha said the tea was 'vulgar and steeped with sea salt.' Marco replied, 'Better vulgar than boiled to death, eh Signora?'"},
    
    {"text": "Q: What did Marco Constantino notice about Eliot Grimsby?\nA: Marco noticed that Eliot’s boots were always clean, 'which is suspicious in a man who claims to walk the orchard every morning.'"},
    
    {"text": "Q: How did Delilah Snipe spend her morning before the murder?\nA: Delilah sat in the bay window rereading her favorite mystery novel, and told Marco, 'Sometimes I think the killer is always the gardener, don’t you?'"},
    
    {"text": "Q: What did Clara Pike say to Marco the day before her death?\nA: Clara said, 'I dreamed last night of an attic full of birds. One sang my name, and the others turned their heads away.' Marco replied gently, 'Poetry again, or prophecy?'"},
    
    {"text": "Q: What was Marco's first impression of Captain Griggs?\nA: Marco said, 'The Captain smells like salt and secrets. A man who’s lost a thumb knows how to hold on to other things.'"},
    
    {"text": "Q: Did anyone see Hugo before the murder?\nA: Marco recalled that Rémy mentioned, 'I passed someone whistling behind the hedge near the kitchen. I thought it might be that fellow Hugo, though I never saw his face.'"},
    
    {"text": "Q: How did Maeve Grimsby describe Marco Constantino?\nA: Maeve once told Delilah, 'Marco walks like he’s solving riddles with each step. And speaks like he's auditioning for a Greek tragedy.'"},
    
    {"text": "Q: What book did Marco bring to the summer house?\nA: Marco brought a worn volume of Dante’s *Inferno*, annotated in the margins with notes like 'Lady Agatha = Second Circle?'"},

    {"text": "Q: What did Dr. Pike and Marco argue about before lunch?\nA: Dr. Pike claimed tooth decay correlated with moral character. Marco replied, 'If rot proved guilt, Doctor, this house would be full of murderers already.'"},
    
    {"text": "Q: What was Marco’s opinion on British weather?\nA: Marco said, 'It rains in your country like a guilty conscience — all at once, then never mentioned again.'"},
]

# Class to wrap SFT data into for training
class LoRA_data:
    def __init__(self):
        self.data = examples
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx): 
        return self.data[idx]
