export interface FamilyMember {
  id: string;
  name: string;
  isAlive: boolean;
  type: 'spouse' | 'child' | 'parent' | 'grandparent';
  side?: 'paternal' | 'maternal';
  children: FamilyMember[];
  spouse?: FamilyMember;
}

export interface InheritanceState {
  deceased: {
    spouse: FamilyMember | null;
    children: FamilyMember[];
    parents: FamilyMember[];
    grandparents: FamilyMember[];
  };
}

export interface FormStepProps {
  onNext: () => void;
  onBack?: () => void;
  updateFamilyTree: (member: FamilyMember) => void;
}

export interface InheritanceCalculation {
  totalEstate: number;
  shares: {
    [key: string]: {
      amount: number;
      percentage: number;
      relationship: string;
    };
  };
} 