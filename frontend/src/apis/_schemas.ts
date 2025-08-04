// schemas.ts

// Common supporting types

/** Shared WorldSetting type */
export interface WorldSetting {
  is_public: boolean;
}

/** CustomField type assumed from your backend code */
export interface CustomField {
  name: string;
  type: string;
  value: string;
  options?: string[];          // optional array
  linked_behavior?: string | null;
}

export const VALID_BLUEPRINT_TYPES = [
  "text",
  "number",
  "boolean",
  "select",
  "blueprint",
] as const;

// BaseDocument shared fields
export interface BaseDocument {
  id: string;
  created_at: Date;
  updated_at?: Date | null;
}


// === Users & Core Entities ===

export interface UserPayload {
  id?: string;
  username?: string;
  email?: string;
  password_current?: string;
  password_new?: string;
  // Note: created_at and updated_at are omitted here per your Python schema
}

export interface UserResponse extends BaseDocument {
  username: string;
  email: string;
  password_current?: string | null;
  password_new?: string | null;
}


// === World ===

export interface WorldPayload {
  id?: string;
  name?: string;
  description?: string;
  creator_id?: string;
  context_ids?: string[];
  blueprint_ids?: string[];
  object_ids?: string[];
  settings?: WorldSetting;
}

export interface WorldResponse extends BaseDocument {
  name: string;
  description?: string | null;
  creator: UserResponse;
  contexts: ContextResponse[];
  blueprints: BlueprintResponse[];
  objects: ObjectResponse[];
  settings: WorldSetting;
}


// === Campaign ===

export interface CampaignPayload {
  id?: string;
  name?: string;
  description?: string;
  creator_id?: string;
  world_id?: string;
  context_ids?: string[];
  blueprint_ids?: string[];
  object_ids?: string[];
  settings?: WorldSetting;
  member_ids?: string[];
  era_ids?: string[];
}

export interface CampaignResponse extends BaseDocument {
  name: string;
  description?: string | null;
  creator: UserResponse;
  world?: WorldResponse | null;
  contexts: ContextResponse[];
  blueprints: BlueprintResponse[];
  objects: ObjectResponse[];
  settings: WorldSetting;
  members: MemberResponse[];
  eras: EraResponse[];
}


// === Member ===

export interface MemberPayload {
  id?: string;
  user_id?: string;
  campaign_id?: string;
  role?: string;
  status?: string;
  sleeve_id?: string;
}

export interface MemberResponse extends BaseDocument {
  user?: UserResponse | null;
  campaign: CampaignResponse;
  role: string;
  status: string;
  sleeve?: ObjectResponse | null;
}


// === Context ===

export interface ContextPayload {
  id?: string;
  name?: string;
  content?: string;
}

export interface ContextResponse extends BaseDocument {
  name: string;
  content: string;
}


// === Blueprint ===

export interface BlueprintPayload {
  id?: string;
  name?: string;
  description?: string;
  creator_id?: string;
  is_public?: boolean;
  is_developer?: boolean;
  fields?: CustomField[];
}

export interface BlueprintResponse extends BaseDocument {
  name: string;
  description?: string | null;
  creator: UserResponse;
  is_public: boolean;
  is_developer: boolean;
  fields: CustomField[];
}


// === Object ===

export interface ObjectPayload {
  id?: string;
  name?: string;
  description?: string;
  creator_id?: string;
  blueprint_id?: string;
  fields?: CustomField[];
}

export interface ObjectResponse extends BaseDocument {
  name: string;
  description?: string | null;
  creator: UserResponse;
  blueprint: BlueprintResponse;
  fields: CustomField[];
}


// === Narrative System ===

export interface ObjectivePayload {
  id?: string;
  name?: string;
  task?: string;
  progress?: number;
  children_ids?: string[];
  parent_id?: string;
}

export interface ObjectiveResponse extends BaseDocument {
  name: string;
  task: string;
  progress: number;
  children: ObjectiveResponse[];
  parent?: ObjectiveResponse | null;
}


export interface EraPayload {
  id?: string;
  campaign_id?: string;
  name?: string;
  description?: string;
  objective_id?: string;
  chapter_ids?: string[];
}

export interface EraResponse extends BaseDocument {
  campaign: CampaignResponse;
  name: string;
  description?: string | null;
  objective: ObjectiveResponse;
  chapters: ChapterResponse[];
}


export interface ChapterPayload {
  id?: string;
  era_id?: string;
  name?: string;
  description?: string;
  objective_id?: string;
  encounter_ids?: string[];
}

export interface ChapterResponse extends BaseDocument {
  era: EraResponse;
  name: string;
  description?: string | null;
  objective: ObjectiveResponse;
  encounters: EncounterResponse[];
}


export interface EncounterPayload {
  id?: string;
  chapter_id?: string;
  name?: string;
  description?: string;
  action_ids?: string[];
}

export interface EncounterResponse extends BaseDocument {
  chapter: ChapterResponse;
  name: string;
  description?: string | null;
  actions: ActionResponse[];
}


// === Action & Events ===

export interface ActionPayload {
  id?: string;
  encounter?: EncounterPayload;  // as you have nested EncounterPayload here, keep optional (or consider id only)
  owner_member_id?: string;
  character_object_id?: string;
  content?: string;
  type?: string;
  dm_response?: string;
  minigame_id?: string;
}

export interface ActionResponse extends BaseDocument {
  encounter: EncounterResponse;
  owner_member: MemberResponse;
  character_object?: ObjectResponse | null;
  content: string;
  type: string;
  dm_response?: string | null;
  minigame?: MinigameResultResponse | null;
}


// === MinigameResult ===

export interface MinigameResultPayload {
  id?: string;
  action_id?: string;
  type?: string;
  result?: string;
  details?: Record<string, any>;
  completed_at?: Date;
}

export interface MinigameResultResponse extends BaseDocument {
  action: ActionResponse;
  type: string;
  result: string;
  details: Record<string, any>;
  completed_at: Date;
}

