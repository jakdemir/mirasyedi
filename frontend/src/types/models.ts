export enum RelationType {
    SPOUSE = 'spouse',
    CHILD = 'child',
    PARENT = 'parent',
    GRANDPARENT = 'grandparent'
}

export enum FamilyBranch {
    DIRECT = 'direct',
    MATERNAL = 'maternal',
    PATERNAL = 'paternal'
}

export interface Heir {
    id: string;
    name: string;
    relation: RelationType;
    is_alive: boolean;
    share?: number;
    children?: Heir[];
    branch?: FamilyBranch;
}

export interface FamilyTree {
    spouse?: Heir;
    children?: Heir[];
    maternal_grandparents?: Heir[];
    paternal_grandparents?: Heir[];
}

export interface Estate {
    total_value: number;
    family_tree: FamilyTree;
}

export interface InheritanceResult {
    estate: Estate;
    error?: string;
}

export interface ApiResponse<T> {
    data: T;
    error?: string;
} 