import { useFamilyTree } from '../context/FamilyTreeContext';
import { FamilyMember } from '../types';

const FamilyTreeDisplay = () => {
  const { familyTree } = useFamilyTree();

  const renderFamilyMember = (member: FamilyMember) => {
    const statusColor = member.isAlive ? 'bg-green-100' : 'bg-red-100';
    const hasChildren = member.children && member.children.length > 0;
    const spouse = member.spouse;

    return (
      <div className={`rounded-lg p-3 ${statusColor} mb-2`}>
        <div className="flex justify-between items-center">
          <div>
            <span className="font-medium">{member.name}</span>
            <span className="ml-2 text-sm text-gray-600">({member.type})</span>
          </div>
          <span className={`text-sm ${member.isAlive ? 'text-green-600' : 'text-red-600'}`}>
            {member.isAlive ? 'Alive' : 'Deceased'}
          </span>
        </div>
        {spouse && (
          <div className="mt-2 pl-4 border-l-2 border-gray-300">
            <div className="text-sm text-gray-600">Spouse:</div>
            <div className={`rounded-lg p-2 ${spouse.isAlive ? 'bg-green-50' : 'bg-red-50'}`}>
              <span className="font-medium">{spouse.name}</span>
              <span className={`ml-2 text-sm ${spouse.isAlive ? 'text-green-600' : 'text-red-600'}`}>
                ({spouse.isAlive ? 'Alive' : 'Deceased'})
              </span>
            </div>
          </div>
        )}
        {hasChildren && member.children && (
          <div className="mt-2 pl-4 border-l-2 border-gray-300">
            <div className="text-sm text-gray-600">Children:</div>
            <div className="space-y-2">
              {member.children.map((child) => (
                <div key={child.id} className="ml-2 text-sm">
                  {renderFamilyMember(child)}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const paternalGrandparents = familyTree.deceased.grandparents.filter(g => g.side === 'paternal');
  const maternalGrandparents = familyTree.deceased.grandparents.filter(g => g.side === 'maternal');

  return (
    <div className="mt-8 bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Family Tree</h2>
      <div className="space-y-6">
        {familyTree.deceased.spouse && (
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Spouse</h3>
            {renderFamilyMember(familyTree.deceased.spouse)}
          </div>
        )}

        {familyTree.deceased.children.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Children</h3>
            {familyTree.deceased.children.map((child) => renderFamilyMember(child))}
          </div>
        )}

        {familyTree.deceased.parents.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Parents</h3>
            {familyTree.deceased.parents.map((parent) => renderFamilyMember(parent))}
          </div>
        )}

        {(paternalGrandparents.length > 0 || maternalGrandparents.length > 0) && (
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Grandparents</h3>
            {paternalGrandparents.length > 0 && (
              <div className="mb-4">
                <h4 className="text-sm font-medium text-gray-600 ml-4 mb-2">
                  Paternal (Father's Parents) {paternalGrandparents.length}/2
                </h4>
                {paternalGrandparents.map((grandparent) => renderFamilyMember(grandparent))}
              </div>
            )}
            {maternalGrandparents.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-600 ml-4 mb-2">
                  Maternal (Mother's Parents) {maternalGrandparents.length}/2
                </h4>
                {maternalGrandparents.map((grandparent) => renderFamilyMember(grandparent))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default FamilyTreeDisplay; 