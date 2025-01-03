export enum RelationType {
    SPOUSE = 'spouse',
    PARENT = 'parent',
    CHILD = 'child',
    GRANDPARENT = 'grandparent'
}

export interface Heir {
    name: string;
    relation: RelationType;
    is_alive: boolean;
    share?: number;
    children?: Heir[];
    side?: 'maternal' | 'paternal';
}

export interface Estate {
    total_value: number;
    heirs: Heir[];
}

export interface InheritanceResult {
    estate: Estate;
    error?: string;
} 