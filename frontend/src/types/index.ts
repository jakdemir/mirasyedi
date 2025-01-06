export enum RelativeType {
  SPOUSE = "spouse",
  CHILD = "child",
  PARENT = "parent",
  GRANDPARENT = "grandparent"
}

export enum ParentType {
  MOTHER = "mother",
  FATHER = "father"
}

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
  share_percentage?: number;
}

export interface FamilyNode {
  person: Person;
  spouse?: Person;
  children: FamilyNode[];
  parents?: {
    [key in ParentType]?: FamilyNode | null;
  };
}

// Color scheme for family tree visualization
export const familyTreeColors = {
  deceased: '#e0e0e0',
  spouse: '#90caf9',
  child: '#81c784',
  parent: '#ffb74d',
  grandparent: '#ce93d8',
  childDeceased: '#c8e6c9',
  parentDeceased: '#ffe0b2',
  grandparentDeceased: '#e1bee7',
} as const;

export interface InheritanceRequest {
  estate_value: number;
  family_tree: FamilyNode;
}

export interface InheritanceShare {
  name: string;
  relation: string;
  share: number;
  share_percentage: number;
}

export interface InheritanceResponse {
  total_distributed: number;
  family_tree: FamilyNode;
  summary: {
    [key: string]: {
      name: string;
      relation: string;
      share: number;
      share_percentage: number;
    };
  };
}

// Form state types
export interface FormStep1Data {
  estate_value: number;
  has_spouse: boolean;
  spouse_name?: string;
  spouse_is_alive: boolean;
}

export interface RelativeData {
  id: string;
  name: string;
  is_alive: boolean;
  type: RelativeType;
  parent_id?: string;
  children?: RelativeData[];
}

// First Degree: Children
export interface FirstDegreeData {
  children: RelativeData[];
}

// Second Degree: Parents and Siblings
export interface SecondDegreeData {
  mother?: RelativeData;
  father?: RelativeData;
  siblings: RelativeData[];
}

// Third Degree: Grandparents and Uncles/Aunts
export interface ThirdDegreeData {
  maternal: {
    grandmother?: RelativeData;
    grandfather?: RelativeData;
    uncles: RelativeData[];
  };
  paternal: {
    grandmother?: RelativeData;
    grandfather?: RelativeData;
    uncles: RelativeData[];
  };
}

export interface FormStep3Data {
  degree: 1 | 2 | 3;
  firstDegree?: FirstDegreeData;
  secondDegree?: SecondDegreeData;
  thirdDegree?: ThirdDegreeData;
} 