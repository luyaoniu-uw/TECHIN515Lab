# TECHIN 515 — Bonus Lab 4.5: Paired wand duel

**Optional inquiry lab.** Work in **pairs**. You use the **magic wand you built in Lab 4** and play a wand duel with a peer. Each student can only participate in the bonus lab at most once.

## Learning objectives

- Extend an edge ML demo into a **multi-device, interactive** experience.
- **Choose and justify** a **wireless** communication approach.
- Design **audience-visible feedback** so a live demo works **from the back of the room** without leaning over your bench.
- Reflect on **latency, reliability, and gesture misclassification** in a real-time setting.

## Hard constraints

1. **Wireless duel** — Spell exchange and duel logic must run over a **wireless** path between the two wand systems (or wand and agreed peer/hub that is not USB-tethered to both wands).  
   - **Does not qualify:** ESP32s plugged into USB on laptop(s) with Serial as the **primary** way moves and outcomes are shared (that is a wired hub, not a wireless duel).  
   

2. **Live demo** — Be ready to run a **short match** in class (order of minutes). Practice **setup, reset, and narration** so the audience follows the story.

3. **Pair work** — Both partners must be able to explain the architecture and point to their contributions (code, wiring, or design doc).

## Suggested game layer (from Lab 4)

Lab 4 ties gestures to spells (see [Lab 4 README](../lab4/README.md)):

| Gesture | Spell (flavor) | Effect (as in Lab 4) |
|--------|----------------|----------------------|
| **Z** | Fire Bolt | Deal **1 HP** to opponent, costs **1 MP** |
| **O** | Reflect Shield | Reflect opponent’s Fire Bolt with **doubled** damage, costs **2 MP** |
| **V** | Healing | **+1 HP** to self, costs **2 MP** |

You may use this full ruleset or **simplify** (e.g. rock–paper–scissors on Z/O/V only) if you **document** your mapping, starting HP/MP, and how simultaneous casts resolve. Spell card artwork referenced in Lab 4 lives under [`../lab4/assets/`](../lab4/assets/) — see [assets/README.md](assets/README.md) in this folder.

## Deliverables


1. **README file**: Justify your wireless choice, topology (peer-to-peer vs hub), why it fits the duel, and what you do when packets are late or gestures mis-fire, along with detailed instructions on how to reproduce your demo.
2. **Live demo** in the scheduled slot (or a pre-approved recorded demo if policy allows).

## Rubric-oriented demo checklist

Your demo will be evaluated on functionality, audience legibility, and creativity and clarity.
