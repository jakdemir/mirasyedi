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

  const rootNode: ApiFamilyNode = {
    person: {
      id: 'deceased',
      name: 'Deceased Person',
      is_alive: false,
      share: 0,
    },
    children: familyTree.deceased.children.map(child => transformMember(child, 'deceased')),
  };

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

  if (familyTree.deceased.parents.length > 0) {
    rootNode.parents = {};
    familyTree.deceased.parents.forEach((parent, index) => {
      const parentType = index === 0 ? 'father' : 'mother';
      rootNode.parents![parentType] = transformMember(parent, 'deceased');
    });
  }

  return {
    estate_value: estateValue,
    family_tree: rootNode,
  };
}; 