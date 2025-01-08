import { FamilyMember, InheritanceState } from '../types';

interface MarriageInfo {
  marriage_order: number;
  is_current: boolean;
}

interface ApiPerson {
  id: string;
  name: string;
  is_alive: boolean;
  parent_id?: string | null;
  marriage_info?: MarriageInfo;
  share: number;
  share_percentage?: number;
}

interface ApiFamilyNode {
  person: ApiPerson;
  spouse?: ApiPerson;
  children: ApiFamilyNode[];
  parents?: Record<string, ApiFamilyNode>;
}

interface ApiRequest {
  estate_value: number;
  family_tree: ApiFamilyNode;
}

export const transformFamilyTreeForApi = (familyTree: InheritanceState, estateValue: number): ApiRequest => {
  const transformMember = (member: FamilyMember, parentId?: string): ApiFamilyNode => {
    const person: ApiPerson = {
      id: member.id,
      name: member.name,
      is_alive: member.isAlive,
      parent_id: parentId || null,
      share: 0,
    };

    if (member.type === 'spouse') {
      person.marriage_info = {
        marriage_order: 1,
        is_current: true,
      };
    }

    const node: ApiFamilyNode = {
      person,
      children: member.children.map(child => transformMember(child, member.id)),
    };

    if (member.spouse) {
      node.spouse = {
        id: member.spouse.id,
        name: member.spouse.name,
        is_alive: member.spouse.isAlive,
        marriage_info: {
          marriage_order: 1,
          is_current: true,
        },
        share: 0,
      };
    }

    return node;
  };

  // Create the root deceased person node
  const rootNode: ApiFamilyNode = {
    person: {
      id: 'deceased',
      name: 'Deceased Person',
      is_alive: false,
      share: 0,
    },
    children: familyTree.deceased.children.map(child => transformMember(child, 'deceased')),
  };

  // Add spouse if exists
  if (familyTree.deceased.spouse) {
    rootNode.spouse = {
      id: familyTree.deceased.spouse.id,
      name: familyTree.deceased.spouse.name,
      is_alive: familyTree.deceased.spouse.isAlive,
      marriage_info: {
        marriage_order: 1,
        is_current: true,
      },
      share: 0,
    };
  }

  // Add parents if they exist
  if (familyTree.deceased.parents.length > 0) {
    rootNode.parents = {};
    familyTree.deceased.parents.forEach((parent, index) => {
      const parentType = index === 0 ? 'father' : 'mother';
      const parentNode = transformMember(parent, 'deceased');

      // Add grandparents for this parent if they exist
      const parentGrandparents = familyTree.deceased.grandparents.filter(g => {
        if (parentType === 'father') {
          return g.side === 'paternal';
        } else {
          return g.side === 'maternal';
        }
      });

      if (parentGrandparents.length > 0) {
        parentNode.parents = {};
        parentGrandparents.forEach((grandparent, gIndex) => {
          const grandparentType = gIndex === 0 ? 'father' : 'mother';
          parentNode.parents![grandparentType] = transformMember(grandparent, parent.id);
        });
      }

      rootNode.parents![parentType] = parentNode;
    });
  }
  // If there are no parents but there are grandparents, create parent nodes
  else if (familyTree.deceased.grandparents.length > 0) {
    rootNode.parents = {};
    
    // Create father node if there are paternal grandparents
    const paternalGrandparents = familyTree.deceased.grandparents.filter(g => g.side === 'paternal');
    if (paternalGrandparents.length > 0) {
      const fatherNode: ApiFamilyNode = {
        person: {
          id: 'father',
          name: 'Father',
          is_alive: false,
          parent_id: 'deceased',
          share: 0,
        },
        children: [],
        parents: {},
      };

      paternalGrandparents.forEach((grandparent, index) => {
        const grandparentType = index === 0 ? 'father' : 'mother';
        fatherNode.parents![grandparentType] = transformMember(grandparent, 'father');
      });

      rootNode.parents['father'] = fatherNode;
    }

    // Create mother node if there are maternal grandparents
    const maternalGrandparents = familyTree.deceased.grandparents.filter(g => g.side === 'maternal');
    if (maternalGrandparents.length > 0) {
      const motherNode: ApiFamilyNode = {
        person: {
          id: 'mother',
          name: 'Mother',
          is_alive: false,
          parent_id: 'deceased',
          share: 0,
        },
        children: [],
        parents: {},
      };

      maternalGrandparents.forEach((grandparent, index) => {
        const grandparentType = index === 0 ? 'father' : 'mother';
        motherNode.parents![grandparentType] = transformMember(grandparent, 'mother');
      });

      rootNode.parents['mother'] = motherNode;
    }
  }

  return {
    estate_value: estateValue,
    family_tree: rootNode,
  };
}; 