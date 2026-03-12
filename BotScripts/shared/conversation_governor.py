from __future__ import annotations

import random
import time
from dataclasses import dataclass, field


@dataclass
class ConversationState:
    active: bool = False
    started_at: float = 0.0
    last_message_at: float = 0.0

    turn_count: int = 0
    bot_turn_count: int = 0
    consecutive_bot_turns: int = 0

    last_bot_id: int | None = None
    exhausted_bots: set[int] = field(default_factory=set)


class ConversationGovernor:
    def __init__(
        self,
        ttl_seconds: float = 18.0,
        max_bot_turns: int = 5,
        max_consecutive_bot_turns: int = 3,
        trigger_bonus: float = 0.20,
        decay_per_turn: float = 0.35,
        min_decay_multiplier: float = 0.10,
    ) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_bot_turns = max_bot_turns
        self.max_consecutive_bot_turns = max_consecutive_bot_turns
        self.trigger_bonus = trigger_bonus
        self.decay_per_turn = decay_per_turn
        self.min_decay_multiplier = min_decay_multiplier

        self.states: dict[int, ConversationState] = {}

    def get_state(self, channel_id: int) -> ConversationState:
        state = self.states.get(channel_id)
        if state is None:
            state = ConversationState()
            self.states[channel_id] = state
        return state

    def _reset_if_expired(self, channel_id: int) -> None:
        state = self.get_state(channel_id)
        now = time.time()

        if state.active and (now - state.last_message_at > self.ttl_seconds):
            self.states[channel_id] = ConversationState()

    def register_human_message(self, channel_id: int) -> None:
        self._reset_if_expired(channel_id)
        state = self.get_state(channel_id)
        now = time.time()

        if not state.active:
            state.active = True
            state.started_at = now

        state.last_message_at = now
        state.turn_count += 1
        state.consecutive_bot_turns = 0
        state.last_bot_id = None
        state.exhausted_bots.clear()

    def can_bot_reply(
        self,
        channel_id: int,
        bot_id: int,
        base_chance: float,
        *,
        is_direct: bool = False,
        is_trigger: bool = False,
    ) -> bool:
        self._reset_if_expired(channel_id)
        state = self.get_state(channel_id)

        if bot_id in state.exhausted_bots and not is_direct:
            return False

        if state.bot_turn_count >= self.max_bot_turns:
            return False

        if state.consecutive_bot_turns >= self.max_consecutive_bot_turns:
            return False

        if state.last_bot_id == bot_id:
            return False

        if is_direct:
            return True

        chance = base_chance
        if is_trigger:
            chance += self.trigger_bonus

        decay_multiplier = max(
            self.min_decay_multiplier,
            1.0 - (self.decay_per_turn * state.consecutive_bot_turns),
        )
        chance *= decay_multiplier
        chance = max(0.0, min(1.0, chance))

        return random.random() < chance

    def register_bot_reply(
        self,
        channel_id: int,
        bot_id: int,
        *,
        dropout_chance: float = 0.0,
    ) -> None:
        self._reset_if_expired(channel_id)
        state = self.get_state(channel_id)
        now = time.time()

        if not state.active:
            state.active = True
            state.started_at = now

        state.last_message_at = now
        state.turn_count += 1
        state.bot_turn_count += 1
        state.consecutive_bot_turns += 1
        state.last_bot_id = bot_id

        if dropout_chance > 0.0 and random.random() < dropout_chance:
            state.exhausted_bots.add(bot_id)

    def end_conversation(self, channel_id: int) -> None:
        self.states[channel_id] = ConversationState()