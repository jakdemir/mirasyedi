export interface MarriageInfo {
    marriage_order: number;
    is_current: boolean;
}

export interface Person {
    id: string;
    name: string;
    is_alive: boolean;
    parent_id?: string;
    marriage_info?: MarriageInfo;
    share: number;
}

export interface FamilyNode {
    person: Person;
    spouse?: Person;
    children: FamilyNode[];
    parents?: Record<'mother' | 'father', FamilyNode | null>;
}

export interface InheritanceRequest {
    estate_value: number;
    family_tree: FamilyNode;
}

export interface InheritanceResponse {
    total_distributed: number;
    shares: Record<string, number>;
}

export interface FamilyTreeFormData {
    name: string;
    is_alive: boolean;
    relation: 'spouse' | 'child' | 'parent' | null;
    parent_id?: string;
    marriage_order?: number;
    is_current_marriage?: boolean;
} 