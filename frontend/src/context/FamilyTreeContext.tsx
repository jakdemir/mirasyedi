import { createContext, useContext, useState, ReactNode } from 'react';
import { FamilyMember, InheritanceState } from '../types';
import { transformFamilyTreeForApi } from '../utils/transformFamilyTree';

interface InheritanceResult {
  total_distributed: number;
  summary: {
    [key: string]: {
      share: number;
      share_percentage: number;
      relationship: string;
    };
  };
}

interface FamilyTreeContextType {
  familyTree: InheritanceState;
  inheritanceResult: InheritanceResult | null;
  estateValue: number;
  addFamilyMember: (member: FamilyMember) => void;
  updateFamilyMember: (id: string, updates: Partial<FamilyMember>) => void;
  removeFamilyMember: (id: string) => void;
  setEstateValue: (value: number) => void;
  calculateInheritance: () => Promise<void>;
}

const FamilyTreeContext = createContext<FamilyTreeContextType | undefined>(undefined);

export const FamilyTreeProvider = ({ children }: { children: ReactNode }) => {
  const [familyTree, setFamilyTree] = useState<InheritanceState>({
    deceased: {
      spouse: null,
      children: [],
      parents: [],
      grandparents: [],
    },
  });

  const [inheritanceResult, setInheritanceResult] = useState<InheritanceResult | null>(null);
  const [estateValue, setEstateValue] = useState<number>(1000);

  const addFamilyMember = (member: FamilyMember) => {
    setFamilyTree((prev) => {
      const newState = { ...prev };
      switch (member.type) {
        case 'spouse':
          newState.deceased.spouse = member;
          break;
        case 'child':
          newState.deceased.children = [...prev.deceased.children, member];
          break;
        case 'parent':
          newState.deceased.parents = [...prev.deceased.parents, member];
          break;
        case 'grandparent':
          newState.deceased.grandparents = [...prev.deceased.grandparents, member];
          break;
      }
      return newState;
    });
  };

  const updateFamilyMember = (id: string, updates: Partial<FamilyMember>) => {
    setFamilyTree((prev) => {
      const newState = { ...prev };
      if (prev.deceased.spouse?.id === id) {
        newState.deceased.spouse = { ...prev.deceased.spouse, ...updates };
      }
      newState.deceased.children = prev.deceased.children.map((child) =>
        child.id === id ? { ...child, ...updates } : child
      );
      newState.deceased.parents = prev.deceased.parents.map((parent) =>
        parent.id === id ? { ...parent, ...updates } : parent
      );
      newState.deceased.grandparents = prev.deceased.grandparents.map((grandparent) =>
        grandparent.id === id ? { ...grandparent, ...updates } : grandparent
      );
      return newState;
    });
  };

  const removeFamilyMember = (id: string) => {
    setFamilyTree((prev) => {
      const newState = { ...prev };
      if (prev.deceased.spouse?.id === id) {
        newState.deceased.spouse = null;
      }
      newState.deceased.children = prev.deceased.children.filter((child) => child.id !== id);
      newState.deceased.parents = prev.deceased.parents.filter((parent) => parent.id !== id);
      newState.deceased.grandparents = prev.deceased.grandparents.filter(
        (grandparent) => grandparent.id !== id
      );
      return newState;
    });
  };

  const calculateInheritance = async () => {
    try {
      const requestData = transformFamilyTreeForApi(familyTree, estateValue);
      const response = await fetch('http://localhost:8000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error('Failed to calculate inheritance');
      }

      const result = await response.json();
      setInheritanceResult(result);
    } catch (error) {
      console.error('Error calculating inheritance:', error);
      throw error;
    }
  };

  return (
    <FamilyTreeContext.Provider
      value={{
        familyTree,
        inheritanceResult,
        estateValue,
        addFamilyMember,
        updateFamilyMember,
        removeFamilyMember,
        setEstateValue,
        calculateInheritance,
      }}
    >
      {children}
    </FamilyTreeContext.Provider>
  );
};

export const useFamilyTree = () => {
  const context = useContext(FamilyTreeContext);
  if (context === undefined) {
    throw new Error('useFamilyTree must be used within a FamilyTreeProvider');
  }
  return context;
}; 