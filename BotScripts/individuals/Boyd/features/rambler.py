import json
import random
from pathlib import Path

from BotScripts.individuals.Boyd.data.static.quotes import quotes


class Rambler:
    def __init__(self):
        self.quotes = quotes

        self.patterns = [
            ["entity", "connector", "accusation"],
            ["entity", "connector", "reveal"],
            ["entity", "connector", "collapse"],
            ["entity", "interruption", "accusation"],
            ["entity", "interruption", "reveal"],
            ["entity", "reaction", "accusation"],
            ["entity", "reaction", "collapse"],
            ["entity", "observation", "reveal"],
            ["entity", "connector", "interruption", "accusation"],
            ["entity", "connector", "interruption", "collapse"],
            ["reaction", "accusation"],
            ["observation", "reveal"],
        ]

        self.accuse_patterns = [
            ["entity", "accusation"],
            ["entity", "connector", "accusation"],
            ["entity", "interruption", "accusation"],
            ["entity", "connector", "reveal"],
            ["entity", "reaction", "accusation"],
            ["entity", "connector", "interruption", "accusation"],
        ]

        self.flow_fallbacks = {
            "entity": ["entity", "observation", "reaction", "reveal"],
            "connector": ["connector", "interruption", "observation"],
            "accusation": ["accusation", "reveal", "reaction", "collapse"],
            "reaction": ["reaction", "accusation", "collapse"],
            "interruption": ["interruption", "reaction", "observation"],
            "collapse": ["collapse", "reaction", "reveal"],
            "reveal": ["reveal", "accusation", "observation"],
            "observation": ["observation", "reaction", "reveal"],
        }

        self.spam_lines = [
            "Are you serious? ARE YOU LISTENING?!",
            "Wait. You just asked me that!",
            "You think repeating it makes it safer?!",
            "Shh! That's how they notice patterns!",
            "No! Too many questions in a row!",
            "I already told you what I know!",
            "Are you buying, or are you spying?",
            "Gah! That's exactly how they test your responses!",
            "You can't just keep pushing the button!",
        ]

        self.repeat_suspect_templates = [
            "{name} again...",
            "Why does {name} keep showing up?!",
            "That one called {name}... again...",
            "I knew it. {name}...",
            "{name}... You see?!",
        ]

        self.memory_path = Path("data/runtime/memory.json")
        self.suspicion_scores = self._load_memory()

    def ramble(self, dynamic_entities=None, favored_entities=None):
        return " ".join(self.ramble_parts(dynamic_entities, favored_entities))

    def ramble_parts(self, dynamic_entities=None, favored_entities=None, force_dynamic_entity=False):
        pattern = random.choice(self.patterns)

        if force_dynamic_entity and "entity" not in pattern:
            pattern = ["entity"] + pattern

        return self._generate_parts(
            pattern=pattern,
            dynamic_entities=dynamic_entities,
            favored_entities=favored_entities,
            forced_entity=None,
            suspect_member_id=None,
            force_dynamic_entity=force_dynamic_entity,
        )

    def accuse_parts(self, forced_entity, dynamic_entities=None, suspect_member_id=None):
        pattern = random.choice(self.accuse_patterns)
        return self._generate_parts(
            pattern=pattern,
            dynamic_entities=dynamic_entities,
            favored_entities=None,
            forced_entity=forced_entity,
            suspect_member_id=suspect_member_id,
            force_dynamic_entity=True,
        )

    def _generate_parts(
            self,
            pattern,
            dynamic_entities=None,
            favored_entities=None,
            forced_entity=None,
            suspect_member_id=None,
            force_dynamic_entity=False,
    ):
        used_ids = set()
        used_dynamic = set()
        parts = []

        selected_member_id = None
        selected_member_name = None
        forced_used = False

        for flow_type in pattern:
            if flow_type == "entity":
                if forced_entity is not None and not forced_used:
                    parts.append(forced_entity["text"])
                    used_dynamic.add(forced_entity["text"])
                    selected_member_id = forced_entity.get("member_id")
                    selected_member_name = forced_entity.get("name")
                    forced_used = True
                    continue

                if dynamic_entities:
                    use_dynamic = force_dynamic_entity or random.random() < 0.90
                    if use_dynamic:
                        entity = self._pick_dynamic_entity(
                            dynamic_entities=dynamic_entities,
                            used_dynamic=used_dynamic,
                            favored_entities=favored_entities,
                        )
                        if entity:
                            parts.append(entity["text"])
                            used_dynamic.add(entity["text"])
                            selected_member_id = entity.get("member_id")
                            selected_member_name = entity.get("name")
                            continue

            entry = self._pick_entry(flow_type, used_ids)
            if entry:
                parts.append(entry["quote"])
                used_ids.add(entry["id"])

        parts = self._post_process(parts)

        if selected_member_id is not None:
            self.record_suspicion(selected_member_id)

            if self.get_suspicion(selected_member_id) >= 3 and selected_member_name:
                if random.random() < 0.35:
                    repeat_line = random.choice(self.repeat_suspect_templates).format(
                        name=selected_member_name
                    )
                    if repeat_line.lower() not in {p.lower() for p in parts}:
                        if random.random() < 0.5:
                            parts.insert(0, repeat_line)
                        else:
                            parts.append(repeat_line)

        if suspect_member_id is not None:
            self.record_suspicion(suspect_member_id)

        return parts

    def spam_response(self):
        if random.random() < 0.7:
            return [random.choice(self.spam_lines)]

        return [
            random.choice(self.spam_lines),
            random.choice([
                "The band manager...",
                "All them haters!",
                "Wait.",
                "Shh! It may be bugged!.",
                "How long do they think they can hide that?!",
            ])
        ]

    def record_suspicion(self, member_id):
        member_id = str(member_id)
        self.suspicion_scores[member_id] = self.suspicion_scores.get(member_id, 0) + 1
        self._save_memory()

    def get_suspicion(self, member_id):
        return self.suspicion_scores.get(str(member_id), 0)

    def decay_suspicion(self, amount=1):
        updated = {}
        for member_id, score in self.suspicion_scores.items():
            new_score = max(0, score - amount)
            if new_score > 0:
                updated[member_id] = new_score
        self.suspicion_scores = updated
        self._save_memory()

    def clear_suspicion(self, member_id=None):
        if member_id is None:
            self.suspicion_scores = {}
        else:
            self.suspicion_scores.pop(str(member_id), None)
        self._save_memory()

    def _pick_dynamic_entity(self, dynamic_entities, used_dynamic, favored_entities=None):
        candidates = [e for e in dynamic_entities if e["text"] not in used_dynamic]
        if not candidates:
            return None

        favored_entities = set(favored_entities or [])
        weights = []

        for candidate in candidates:
            weight = 1.0

            if candidate["text"] in favored_entities:
                weight *= 4.0

            member_id = candidate.get("member_id")
            if member_id is not None:
                suspicion = self.get_suspicion(member_id)
                weight *= (1.0 + min(suspicion * 0.75, 6.0))

            weights.append(weight)

        return random.choices(candidates, weights=weights, k=1)[0]

    def _pick_entry(self, flow_type, used_ids):
        candidate_flows = self.flow_fallbacks.get(flow_type, [flow_type])

        candidates = []
        for quote_id, entry in self.quotes.items():
            if quote_id in used_ids:
                continue

            entry_flows = entry.get("flow", [])
            if not any(flow in entry_flows for flow in candidate_flows):
                continue

            weight = entry.get("weight", 1)
            if flow_type in entry_flows:
                weight *= 1.5

            candidates.append({
                "id": quote_id,
                "quote": entry["quote"],
                "weight": weight,
            })

        if not candidates:
            return None

        return random.choices(
            candidates,
            weights=[c["weight"] for c in candidates],
            k=1
        )[0]

    def _post_process(self, parts):
        cleaned = []
        seen = set()

        for part in parts:
            normalized = part.strip().lower()
            if not normalized:
                continue
            if normalized in seen:
                continue
            cleaned.append(part)
            seen.add(normalized)

        return cleaned

    def _load_memory(self):
        try:
            self.memory_path.parent.mkdir(parents=True, exist_ok=True)

            if not self.memory_path.exists():
                self.memory_path.write_text("{}", encoding="utf-8")
                return {}

            raw = self.memory_path.read_text(encoding="utf-8").strip()
            if not raw:
                return {}

            data = json.loads(raw)
            if isinstance(data, dict):
                cleaned = {}
                for key, value in data.items():
                    try:
                        cleaned[str(key)] = int(value)
                    except (TypeError, ValueError):
                        continue
                return cleaned

            return {}
        except (OSError, json.JSONDecodeError):
            return {}

    def _save_memory(self):
        try:
            self.memory_path.parent.mkdir(parents=True, exist_ok=True)
            self.memory_path.write_text(
                json.dumps(self.suspicion_scores, indent=2, sort_keys=True),
                encoding="utf-8",
            )
        except OSError:
            pass