import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Switch } from '@headlessui/react';
import { FamilyMember } from '../../types';
import { useFamilyTree } from '../../context/FamilyTreeContext';

const ChildForm = ({ member, onUpdate }: { member: FamilyMember; onUpdate: (updates: Partial<FamilyMember>) => void }) => {
  const [name, setName] = useState('');
  const [isAlive, setIsAlive] = useState(true);
  const [relation, setRelation] = useState<'spouse' | 'child'>('child');

  const handleAdd = () => {
    if (!name.trim()) return;

    const newMember: FamilyMember = {
      id: crypto.randomUUID(),
      name: name.trim(),
      isAlive,
      type: relation,
      children: [],
    };

    if (relation === 'spouse') {
      onUpdate({ spouse: newMember });
    } else {
      const updatedChildren = [...(member.children || []), newMember];
      onUpdate({ children: updatedChildren });
    }

    setName('');
    setIsAlive(true);
    setRelation('child');
  };

  return (
    <div className="space-y-4 pl-6 border-l-2 border-gray-200">
      {!member.spouse && (
        <div>
          <label className="block text-sm font-medium text-gray-700">Relation</label>
          <select
            value={relation}
            onChange={(e) => setRelation(e.target.value as 'spouse' | 'child')}
            className="form-input mt-1"
          >
            <option value="child">Child</option>
            <option value="spouse">Spouse</option>
          </select>
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-700">Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="form-input mt-1"
          placeholder="Enter name"
        />
      </div>

      <div className="flex items-center space-x-4">
        <span className="text-sm font-medium text-gray-700">Status</span>
        <Switch.Group>
          <div className="flex items-center">
            <Switch.Label className="mr-3 text-sm text-gray-500">Deceased</Switch.Label>
            <Switch
              checked={isAlive}
              onChange={setIsAlive}
              className={`${
                isAlive ? 'bg-indigo-600' : 'bg-gray-200'
              } relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2`}
            >
              <span
                className={`${
                  isAlive ? 'translate-x-6' : 'translate-x-1'
                } inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
              />
            </Switch>
            <Switch.Label className="ml-3 text-sm text-gray-500">Alive</Switch.Label>
          </div>
        </Switch.Group>
      </div>

      <div>
        <button type="button" onClick={handleAdd} className="btn-primary">
          Add {!member.spouse ? (relation === 'spouse' ? 'Spouse' : 'Child') : 'Child'}
        </button>
      </div>

      {member.spouse && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h4 className="text-sm font-medium text-gray-900">Spouse</h4>
          <div className="mt-2">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">{member.spouse.name}</p>
                <p className="text-sm text-gray-500">
                  Status: {member.spouse.isAlive ? 'Alive' : 'Deceased'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {member.children && member.children.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h4 className="text-sm font-medium text-gray-900">Children</h4>
          <div className="mt-2 space-y-2">
            {member.children.map((child) => (
              <div key={child.id} className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">{child.name}</p>
                  <p className="text-sm text-gray-500">
                    Status: {child.isAlive ? 'Alive' : 'Deceased'}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const ChildrenForm = () => {
  const navigate = useNavigate();
  const { familyTree, addFamilyMember, updateFamilyMember, removeFamilyMember, calculateInheritance } = useFamilyTree();
  const [childName, setChildName] = useState('');
  const [isAlive, setIsAlive] = useState(true);
  const [isCalculating, setIsCalculating] = useState(false);
  const [calculationError, setCalculationError] = useState<string | null>(null);

  const handleAddChild = () => {
    if (!childName.trim()) return;

    const newChild: FamilyMember = {
      id: crypto.randomUUID(),
      name: childName.trim(),
      isAlive,
      type: 'child',
      children: [],
    };

    addFamilyMember(newChild);
    setChildName('');
    setIsAlive(true);
  };

  const handleRemoveChild = (id: string) => {
    removeFamilyMember(id);
  };

  const handleCalculate = async () => {
    try {
      setCalculationError(null);
      setIsCalculating(true);
      await calculateInheritance();
    } catch (error) {
      console.error('Error calculating inheritance:', error);
      setCalculationError('Failed to calculate inheritance. Please try again.');
    } finally {
      setIsCalculating(false);
    }
  };

  return (
    <div className="space-y-8 divide-y divide-gray-200">
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-medium leading-6 text-gray-900">Children Information</h3>
          <p className="mt-1 text-sm text-gray-500">
            Please provide information about the children.
          </p>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="child-name" className="block text-sm font-medium text-gray-700">
              Child Name
            </label>
            <input
              type="text"
              id="child-name"
              value={childName}
              onChange={(e) => setChildName(e.target.value)}
              className="form-input mt-1"
              placeholder="Enter child name"
            />
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-sm font-medium text-gray-700">Status</span>
            <Switch.Group>
              <div className="flex items-center">
                <Switch.Label className="mr-3 text-sm text-gray-500">Deceased</Switch.Label>
                <Switch
                  checked={isAlive}
                  onChange={setIsAlive}
                  className={`${
                    isAlive ? 'bg-indigo-600' : 'bg-gray-200'
                  } relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2`}
                >
                  <span
                    className={`${
                      isAlive ? 'translate-x-6' : 'translate-x-1'
                    } inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
                  />
                </Switch>
                <Switch.Label className="ml-3 text-sm text-gray-500">Alive</Switch.Label>
              </div>
            </Switch.Group>
          </div>

          {calculationError && (
            <div className="text-sm text-red-600">{calculationError}</div>
          )}

          <div className="flex justify-between">
            <button
              type="button"
              onClick={handleAddChild}
              className="btn-primary"
            >
              Add Child
            </button>
            <div className="space-x-4">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="btn-secondary"
              >
                Back
              </button>
              {familyTree.deceased.children.length === 0 ? (
                <button
                  type="button"
                  onClick={() => navigate('/parents')}
                  className="btn-primary"
                >
                  Next: Parents
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleCalculate}
                  className="btn-primary"
                  disabled={isCalculating}
                >
                  {isCalculating ? 'Calculating...' : 'Calculate Inheritance'}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {familyTree.deceased.children.length > 0 && (
        <div className="pt-6">
          <h4 className="text-sm font-medium text-gray-900">Added Children</h4>
          <div className="mt-4 divide-y divide-gray-200">
            {familyTree.deceased.children.map((child) => (
              <div key={child.id}>
                <div
                  className={`flex items-center justify-between py-4 ${
                    !child.isAlive ? 'bg-gray-50' : ''
                  }`}
                >
                  <div>
                    <p className="text-sm font-medium text-gray-900">{child.name}</p>
                    <p className="text-sm text-gray-500">
                      Status: {child.isAlive ? 'Alive' : 'Deceased'}
                    </p>
                    {!child.isAlive && child.children && child.children.length > 0 && (
                      <p className="mt-1 text-sm text-gray-500">
                        Children: {child.children.length}
                      </p>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveChild(child.id)}
                    className="text-sm text-red-600 hover:text-red-900"
                  >
                    Remove
                  </button>
                </div>
                {!child.isAlive && (
                  <div className="animate-slide-down">
                    <ChildForm
                      member={child}
                      onUpdate={(updates) => updateFamilyMember(child.id, updates)}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChildrenForm; 