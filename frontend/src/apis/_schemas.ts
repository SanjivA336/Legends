// schemas.ts

export type WorldSetting = {
  is_public: boolean;
};

// BaseDocument for shared fields
export interface BaseDocument {
  id: string;
  created_at: Date;
  updated_at?: Date | null;
}

// === Users & Core Entities ===

export interface UserPayload extends Partial<BaseDocument> {
  username?: string;
  email?: string;
  password_current?: string;
  password_new?: string;
}

export interface UserResponse extends BaseDocument {
  username: string;
  email: string;
  password_current?: string | null;
  password_new?: string | null;
}

// === World ===

export interface WorldPayload extends Partial<BaseDocument> {
  name?: string;
  description?: string | null;
  creator?: UserPayload | null;
  contexts?: ContextPayload[] | null;
  settings?: WorldSetting | null;
}

export interface WorldResponse extends BaseDocument {
  name: string;
  description?: string | null;
  creator: UserResponse;
  contexts: ContextResponse[];
  settings: WorldSetting;
}


// === Campaign ===

export interface CampaignPayload extends Partial<BaseDocument> {
  name?: string;
  description?: string | null;
  creator?: UserPayload | null;
  world?: WorldPayload | null;
  contexts?: ContextPayload[] | null;
  settings?: WorldSetting | null;
  members?: MemberPayload[] | null;
  eras?: EraPayload[] | null;
}

export interface CampaignResponse extends BaseDocument {
  name: string;
  description?: string | null;
  creator: UserResponse;
  world?: WorldResponse | null;
  contexts: ContextResponse[];
  settings: WorldSetting;
  members: MemberResponse[];
  eras: EraResponse[];
}

// === Member ===

export interface MemberPayload extends Partial<BaseDocument> {
  user?: UserPayload | null;
  campaign?: CampaignPayload | null;
  role?: string;
  status?: string;
  sleeve?: ObjectPayload | null;
}

export interface MemberResponse extends BaseDocument {
  user?: UserResponse | null;
  campaign: CampaignResponse;
  role: string;
  status: string;
  sleeve?: ObjectResponse | null;
}

// === Context ===
export interface ContextPayload extends Partial<BaseDocument> {
  name?: string;
  type?: string;
  data?: Record<string, any>;
}

export interface ContextResponse extends BaseDocument {
  name: string;
  type: string;
  data: Record<string, any>;
}

// === Blueprint System ===
export interface CustomField {
  name: string;
  type: string;
  value: string;
  options?: string[] | null;
  linked_behavior?: string | null;
}

export interface BlueprintPayload extends Partial<BaseDocument> {
  name?: string;
  description?: string | null;
  creator?: UserPayload | null;
  is_public?: boolean;
  is_developer?: boolean;
  fields?: CustomField[] | null;
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

export interface ObjectPayload extends Partial<BaseDocument> {
  name?: string;
  description?: string | null;
  creator?: UserPayload | null;
  blueprint?: BlueprintPayload | null;
  fields?: CustomField[] | null;
}

export interface ObjectResponse extends BaseDocument {
  name: string;
  description?: string | null;
  creator: UserResponse;
  blueprint: BlueprintResponse;
  fields: CustomField[];
}


// === Narrative System ===

export interface ObjectivePayload extends Partial<BaseDocument> {
  name?: string;
  task?: string;
  progress?: number;
  children?: ObjectivePayload[] | null;
  parent?: ObjectivePayload | null;
}

export interface ObjectiveResponse extends BaseDocument {
  name: string;
  task: string;
  progress: number;
  children: ObjectiveResponse[];
  parent?: ObjectiveResponse | null;
}

export interface EraPayload extends Partial<BaseDocument> {
  campaign?: CampaignPayload | null;
  name?: string;
  description?: string | null;
  objective?: ObjectivePayload | null;
  chapters?: ChapterPayload[] | null;
}

export interface EraResponse extends BaseDocument {
  campaign: CampaignResponse;
  name: string;
  description?: string | null;
  objective: ObjectiveResponse;
  chapters: ChapterResponse[];
}

export interface ChapterPayload extends Partial<BaseDocument> {
  era?: EraPayload | null;
  name?: string;
  description?: string | null;
  objective?: ObjectivePayload | null;
  encounters?: EncounterPayload[] | null;
}

export interface ChapterResponse extends BaseDocument {
  era: EraResponse;
  name: string;
  description?: string | null;
  objective: ObjectiveResponse;
  encounters: EncounterResponse[];
}

export interface EncounterPayload extends Partial<BaseDocument> {
  chapter?: ChapterPayload | null;
  name?: string;
  description?: string | null;
  actions?: ActionPayload[] | null;
}

export interface EncounterResponse extends BaseDocument {
  chapter: ChapterResponse;
  name: string;
  description?: string | null;
  actions: ActionResponse[];
}

// === Gameplay & Events ===

export interface ActionPayload extends Partial<BaseDocument> {
  encounter?: EncounterPayload | null;
  owner_member?: MemberPayload | null;
  character_object?: ObjectPayload | null;
  content?: string;
  type?: string;
  dm_response?: string | null;
  minigame?: MinigameResultPayload | null;
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

export interface MinigameResultPayload extends Partial<BaseDocument> {
  action?: ActionPayload | null;
  type?: string;
  result?: string;
  details?: Record<string, any> | null;
  completed_at?: Date | null;
}

export interface MinigameResultResponse extends BaseDocument {
  action: ActionResponse;
  type: string;
  result: string;
  details: Record<string, any>;
  completed_at: Date;
}
