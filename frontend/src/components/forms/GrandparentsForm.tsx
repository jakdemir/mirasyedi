import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Switch } from '@headlessui/react';
import { FamilyMember, InheritanceCalculation } from '../../types';
import { useFamilyTree } from '../../context/FamilyTreeContext';

const ChildForm = ({ member, onUpdate }: { member: FamilyMember; onUpdate: (updates: Partial<FamilyMember>) => void }) => {
  const [name, setName] = useState('');
  const [isAlive, setIsAlive] = useState(true);

  const handleAdd = () => {
    if (!name.trim()) return;

    const newMember: FamilyMember = {
      id: crypto.randomUUID(),
      name: name.trim(),
      isAlive,
      type: 'child',
      children: [],
    };

    const updatedChildren = [...(member.children || []), newMember];
    onUpdate({ children: updatedChildren });

    setName('');
    setIsAlive(true);
  };

  return (
    <div className="space-y-4 pl-6 border-l-2 border-gray-200">
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
          Add Child
        </button>
      </div>

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

const GrandparentsForm = () => {
  const navigate = useNavigate();
  const { familyTree, addFamilyMember, updateFamilyMember, removeFamilyMember } = useFamilyTree();

  useEffect(() => {
    // Redirect to children page if there are any children
    if (familyTree.deceased.children.length > 0) {
      navigate('/children');
    }
  }, [familyTree.deceased.children.length, navigate]);

  const [grandparentName, setGrandparentName] = useState('');
  const [isAlive, setIsAlive] = useState(true);
  const [side, setSide] = useState<'paternal' | 'maternal'>('paternal');
  const [calculationResult, setCalculationResult] = useState<InheritanceCalculation | null>(null);
  const [calculationError, setCalculationError] = useState<string | null>(null);

  const handleAddGrandparent = () => {
    if (!grandparentName.trim()) return;

    const sideGrandparents = familyTree.deceased.grandparents.filter(g => g.side === side);
    if (sideGrandparents.length >= 2) {
      return; // Don't add if we already have 2 grandparents for this side
    }

    const newGrandparent: FamilyMember = {
      id: crypto.randomUUID(),
      name: grandparentName.trim(),
      isAlive,
      type: 'grandparent',
      side,
      children: [],
    };

    addFamilyMember(newGrandparent);
    setGrandparentName('');
    setIsAlive(true);
  };

  const handleRemoveGrandparent = (id: string) => {
    removeFamilyMember(id);
  };

  const handleCalculate = async () => {
    try {
      setCalculationError(null);
      const response = await fetch('/api/calculate-inheritance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(familyTree),
      });

      if (!response.ok) {
        throw new Error('Failed to calculate inheritance');
      }

      const result = await response.json();
      setCalculationResult(result);
    } catch (error) {
      console.error('Error calculating inheritance:', error);
      setCalculationError('Failed to calculate inheritance. Please try again.');
    }
  };

  const paternalGrandparents = familyTree.deceased.grandparents.filter(g => g.side === 'paternal');
  const maternalGrandparents = familyTree.deceased.grandparents.filter(g => g.side === 'maternal');

  // Check if current side has reached its limit
  const currentSideGrandparents = side === 'paternal' ? paternalGrandparents : maternalGrandparents;
  const isCurrentSideFull = currentSideGrandparents.length >= 2;

  return (
    <div className="space-y-8 divide-y divide-gray-200">
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-medium leading-6 text-gray-900">Grandparents Information</h3>
          <p className="mt-1 text-sm text-gray-500">
            Please provide information about the grandparents. Maximum two grandparents per side (paternal/maternal).
          </p>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Side</label>
            <select
              value={side}
              onChange={(e) => setSide(e.target.value as 'paternal' | 'maternal')}
              className="form-input mt-1"
            >
              <option value="paternal">Paternal (Father's Parents) {paternalGrandparents.length}/2</option>
              <option value="maternal">Maternal (Mother's Parents) {maternalGrandparents.length}/2</option>
            </select>
          </div>

          <div>
            <label htmlFor="grandparent-name" className="block text-sm font-medium text-gray-700">
              Grandparent Name
            </label>
            <input
              type="text"
              id="grandparent-name"
              value={grandparentName}
              onChange={(e) => setGrandparentName(e.target.value)}
              className="form-input mt-1"
              placeholder="Enter grandparent name"
              disabled={isCurrentSideFull}
            />
            {isCurrentSideFull && (
              <p className="mt-1 text-sm text-red-500">
                Maximum number of {side} grandparents reached (2/2)
              </p>
            )}
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
              onClick={handleAddGrandparent}
              className="btn-primary"
              disabled={isCurrentSideFull}
            >
              Add Grandparent
            </button>
            <div className="space-x-4">
              <button
                type="button"
                onClick={() => navigate('/parents')}
                className="btn-secondary"
              >
                Back
              </button>
              <button
                type="button"
                onClick={handleCalculate}
                className="btn-primary"
                disabled={familyTree.deceased.grandparents.length === 0}
              >
                Calculate Inheritance
              </button>
            </div>
          </div>
        </div>
      </div>

      {paternalGrandparents.length > 0 && (
        <div className="pt-6">
          <h4 className="text-sm font-medium text-gray-900">
            Paternal Grandparents (Father's Parents) {paternalGrandparents.length}/2
          </h4>
          <div className="mt-4 divide-y divide-gray-200">
            {paternalGrandparents.map((grandparent) => (
              <div key={grandparent.id}>
                <div className="flex items-center justify-between py-4">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{grandparent.name}</p>
                    <p className="text-sm text-gray-500">
                      Status: {grandparent.isAlive ? 'Alive' : 'Deceased'}
                    </p>
                    {!grandparent.isAlive && grandparent.children && grandparent.children.length > 0 && (
                      <p className="mt-1 text-sm text-gray-500">
                        Children: {grandparent.children.length}
                      </p>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveGrandparent(grandparent.id)}
                    className="text-sm text-red-600 hover:text-red-900"
                  >
                    Remove
                  </button>
                </div>
                {!grandparent.isAlive && (
                  <div className="animate-slide-down">
                    <ChildForm
                      member={grandparent}
                      onUpdate={(updates) => updateFamilyMember(grandparent.id, updates)}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {maternalGrandparents.length > 0 && (
        <div className="pt-6">
          <h4 className="text-sm font-medium text-gray-900">
            Maternal Grandparents (Mother's Parents) {maternalGrandparents.length}/2
          </h4>
          <div className="mt-4 divide-y divide-gray-200">
            {maternalGrandparents.map((grandparent) => (
              <div key={grandparent.id}>
                <div className="flex items-center justify-between py-4">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{grandparent.name}</p>
                    <p className="text-sm text-gray-500">
                      Status: {grandparent.isAlive ? 'Alive' : 'Deceased'}
                    </p>
                    {!grandparent.isAlive && grandparent.children && grandparent.children.length > 0 && (
                      <p className="mt-1 text-sm text-gray-500">
                        Children: {grandparent.children.length}
                      </p>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveGrandparent(grandparent.id)}
                    className="text-sm text-red-600 hover:text-red-900"
                  >
                    Remove
                  </button>
                </div>
                {!grandparent.isAlive && (
                  <div className="animate-slide-down">
                    <ChildForm
                      member={grandparent}
                      onUpdate={(updates) => updateFamilyMember(grandparent.id, updates)}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {calculationResult && (
        <div className="pt-6">
          <h4 className="text-lg font-medium text-gray-900">Inheritance Calculation Results</h4>
          <div className="mt-4 bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
                <div className="sm:col-span-2">
                  <dt className="text-sm font-medium text-gray-500">Total Estate</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    ${calculationResult.totalEstate.toLocaleString()}
                  </dd>
                </div>
                {Object.entries(calculationResult.shares).map(([id, share]) => (
                  <div key={id}>
                    <dt className="text-sm font-medium text-gray-500">{share.relationship}</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      ${share.amount.toLocaleString()} ({share.percentage}%)
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>
      )}

      {calculationError && (
        <div className="pt-6">
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{calculationError}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GrandparentsForm; 