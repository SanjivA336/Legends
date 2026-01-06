// === === Config === ===
export const EMPTY_STRING = "";
export const UNKNOWN = "Unknown";
export const UNNAMED = "Unnamed";

// === === Base === ===
export interface BaseDocument {
    id: string;
    createdAt: string;  // ISO datetime
    updatedAt: string;
}

// === === Identification Models === ===
export interface User extends BaseDocument {
    email: string;
    username: string;
    memberIds: string[];
    worldIds: string[];
    campaignIds: string[];
}

export interface Member extends BaseDocument {
    userId?: string;
    campaignId: string;
    isAdmin: boolean;
    isDm: boolean;
    isActive: boolean;
    characterId?: string;
    equippedIds: string[];
    inventoryIds: string[];
}

// === === Game Setting Models === ===
export interface World extends BaseDocument {
    name: string;
    description?: string;
    settings: Record<string, any>;
    blueprintIds: string[];
    objectIds: string[];
    contextIds: string[];
}

export interface Campaign extends BaseDocument {
    worldId: string;
    name: string;
    description?: string;
    settings: Record<string, any>;
    memberIds: string[];
    blueprintIds: string[];
    objectIds: string[];
    contextIds: string[];
    questIds: string[];
}

// === === Content Models === ===
export const AttributeType = {
    STRING: "string",
    NUMBER: "number",
    BOOLEAN: "boolean",
    OBJECT: "object",
} as const;
export type AttributeType = typeof AttributeType[keyof typeof AttributeType];

export interface Attribute {
    name: string;
    type: AttributeType;
    values: any[];
    options?: any[];
    isRequired: boolean;
    isList: boolean;
    isDropdown: boolean;
    attributeBinding?: string;
}

export const BlueprintBinding = {
    PLAYER_CHARACTER: "pc",
    NON_PLAYER_CHARACTER: "npc",
    RACE: "race",
    ANIMAL: "animal",
    FACTION: "faction",
    WEAPON: "weapon",
    ABILITY: "ability",
    ARMOR: "armor",
    ACCESSORY: "accessory",
    TOOL: "tool",
    CURRENCY: "currency",
    CONSUMABLE: "consumable",
    ITEM: "item",
    STATUS: "status",
    CONDITION: "condition",
    LOCATION: "location",
    VEHICLE: "vehicle",
} as const;
export type BlueprintBinding = typeof BlueprintBinding[keyof typeof BlueprintBinding];

export interface Blueprint extends BaseDocument {
    name: string;
    description?: string;
    blueprintBinding?: BlueprintBinding;
    attributes: Attribute[];
}

export interface Object extends BaseDocument {
    blueprintId?: string;
    name: string;
    description?: string;
    blueprintBinding?: BlueprintBinding;
    attributes: Attribute[];
}

export interface Context extends BaseDocument {
    name: string;
    content: string;
}

export interface Quest extends BaseDocument {
    name: string;
    description?: string;
    task: string;
    isMain: boolean;
    isActive: boolean;
    isComplete: boolean;
    parentId?: string;
    childrenIds: string[];
}

// === === Timeline Models ===
export const ActionType = {
    WAIT: "wait",
    ATTACK: "attack",
    DEFEND: "defend",
    DODGE: "dodge",
    MOVE: "move",
    ADV_MOVE: "adv_move",
    SNEAK: "sneak",
    PERSUADE: "persuade",
    INTIMIDATE: "intimidate",
    ANTAGONIZE: "antagonize",
    DECEIVE: "deceive",
    ACTIVATE: "activate",
    USE_ITEM: "use_item",
    CAST: "cast",
    INTERACT: "interact",
    INVESTIGATE: "investigate",
    SIMPLE: "simple",
    IMPOSSIBLE: "impossible",
} as const;
export type ActionType = typeof ActionType[keyof typeof ActionType];

export const ActionStatus = {
    WAITING: "waiting",
    ROLLING: "rolling",
    DENIED: "denied",
    CRIT_FAILURE: "crit_failure",
    FAILURE: "failure",
    SUCCESS: "success",
    CRIT_SUCCESS: "crit_success",
} as const;
export type ActionStatus = typeof ActionStatus[keyof typeof ActionStatus];

export interface Action {
    memberId: string;
    type?: ActionType;
    intent: string;
    status: ActionStatus;
    itemIds: string[];
    targetIds: string[];
    requirement?: number;
}

export interface Scene extends BaseDocument {
    campaignId: string;
    encounterId: string;
    content: string;
    summary?: string;
    actions: Action[];
    minuteTime: number;
}

export const EncounterType = {
    COMBAT: "combat",
    EXPLORATION: "exploration",
    SOCIAL: "social",
    PUZZLE: "puzzle",
    STORE: "store",
    TRAVEL: "travel",
    MISC: "miscellaneous",
} as const;
export type EncounterType = typeof EncounterType[keyof typeof EncounterType];

export interface Encounter extends BaseDocument {
    campaignId: string;
    chapterId: string;
    type: EncounterType;
    goal: string;
    length: number;
    sceneIds: string[];
}

export interface Chapter extends BaseDocument {
    campaignId: string;
    description?: string;
    encounterIds: string[];
}