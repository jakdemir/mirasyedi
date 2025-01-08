import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Switch } from '@headlessui/react';
import { FamilyMember } from '../../types';
import { useFamilyTree } from '../../context/FamilyTreeContext';

const SpouseForm = () => {
  const navigate = useNavigate();
  const { familyTree, addFamilyMember, removeFamilyMember } = useFamilyTree();
  const [spouseName, setSpouseName] = useState('');
  const [isAlive, setIsAlive] = useState(true);

  const handleAddSpouse = () => {
    if (!spouseName.trim()) return;

    const newSpouse: FamilyMember = {
      id: crypto.randomUUID(),
      name: spouseName.trim(),
      isAlive,
      type: 'spouse',
    };

    addFamilyMember(newSpouse);
    setSpouseName('');
    setIsAlive(true);
  };

  const handleRemoveSpouse = (id: string) => {
    removeFamilyMember(id);
  };

  return (
    <div className="space-y-8 divide-y divide-gray-200">
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-medium leading-6 text-gray-900">Spouse Information</h3>
          <p className="mt-1 text-sm text-gray-500">
            Please provide information about the spouse(s).
          </p>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="spouse-name" className="block text-sm font-medium text-gray-700">
              Spouse Name
            </label>
            <input
              type="text"
              id="spouse-name"
              value={spouseName}
              onChange={(e) => setSpouseName(e.target.value)}
              className="form-input mt-1"
              placeholder="Enter spouse name"
              disabled={familyTree.deceased.spouse !== undefined}
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
            <button
              type="button"
              onClick={handleAddSpouse}
              className="btn-primary"
              disabled={familyTree.deceased.spouse !== undefined}
            >
              Add Spouse
            </button>
            <button
              type="button"
              onClick={() => navigate('/children')}
              className="btn-secondary"
              disabled={familyTree.deceased.spouse === undefined}
            >
              Next: Children
            </button>
          </div>
        </div>
      </div>

      {familyTree.deceased.spouse && (
        <div className="pt-6">
          <h4 className="text-sm font-medium text-gray-900">Added Spouse</h4>
          <div className="mt-4">
            <div className="flex items-center justify-between py-4">
              <div>
                <p className="text-sm font-medium text-gray-900">{familyTree.deceased.spouse.name}</p>
                <p className="text-sm text-gray-500">
                  Status: {familyTree.deceased.spouse.isAlive ? 'Alive' : 'Deceased'}
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleRemoveSpouse(familyTree.deceased.spouse!.id)}
                className="text-sm text-red-600 hover:text-red-900"
              >
                Remove
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SpouseForm; 