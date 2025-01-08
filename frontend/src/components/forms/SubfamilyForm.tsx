import { useState } from 'react';
import { Switch } from '@headlessui/react';
import { FamilyMember } from '../../types';
import { useFamilyTree } from '../../context/FamilyTreeContext';

interface SubfamilyFormProps {
  member: FamilyMember;
  onClose: () => void;
}

const SubfamilyForm = ({ member, onClose }: SubfamilyFormProps) => {
  const { updateFamilyMember } = useFamilyTree();
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
      updateFamilyMember(member.id, { spouse: newMember });
    } else {
      const updatedChildren = [...(member.children || []), newMember];
      updateFamilyMember(member.id, { children: updatedChildren });
    }

    setName('');
    setIsAlive(true);
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium leading-6 text-gray-900">
          Add Family Member for {member.name}
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Add spouse or children for the deceased family member.
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Relation</label>
          <select
            value={relation}
            onChange={(e) => setRelation(e.target.value as 'spouse' | 'child')}
            className="form-input mt-1"
          >
            <option value="child">Child</option>
            {!member.spouse && <option value="spouse">Spouse</option>}
          </select>
        </div>

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

        <div className="flex justify-between">
          <button type="button" onClick={handleAdd} className="btn-primary">
            Add {relation === 'spouse' ? 'Spouse' : 'Child'}
          </button>
          <button type="button" onClick={onClose} className="btn-secondary">
            Close
          </button>
        </div>
      </div>

      {member.spouse && (
        <div className="pt-4 border-t border-gray-200">
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
        <div className="pt-4 border-t border-gray-200">
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

export default SubfamilyForm; 