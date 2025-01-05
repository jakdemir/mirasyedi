import React, { useState } from 'react';
import { HeirForm } from '../components/HeirForm';
import { HeirList } from '../components/HeirList';
import { Estate, Heir, RelationType, FamilyTree } from '../types';
import { calculateInheritance } from '../services/api';

const RELATION_TYPES = {
    SPOUSE: 'spouse' as RelationType,
    CHILD: 'child' as RelationType,
    GRANDCHILD: 'grandchild' as RelationType,
    PARENT: 'parent' as RelationType,
    GRANDPARENT: 'grandparent' as RelationType
} as const;

export const Calculator: React.FC = () => {
    const [estate, setEstate] = useState<Estate>({
        total_value: 1000,
        family_tree: {
            children: [],
            mother: undefined,
            father: undefined,
            maternal_grandparents: [],
            paternal_grandparents: []
        }
    });
    const [error, setError] = useState<string>();
    const [loading, setLoading] = useState(false);

    const hasSpouse = Boolean(estate.family_tree.spouse);
    const hasChildren = Boolean(estate.family_tree.children && estate.family_tree.children.length > 0);
    const hasParents = Boolean(estate.family_tree.mother || estate.family_tree.father);
    const hasAnyHeirs = Boolean(
        hasSpouse || 
        hasChildren ||
        hasParents ||
        (estate.family_tree.maternal_grandparents && estate.family_tree.maternal_grandparents.length > 0) ||
        (estate.family_tree.paternal_grandparents && estate.family_tree.paternal_grandparents.length > 0)
    );

    const handleAddHeir = (heir: Heir) => {
        setEstate(prev => {
            const newFamilyTree = { ...prev.family_tree };
            
            switch (heir.relation) {
                case RELATION_TYPES.SPOUSE:
                    newFamilyTree.spouse = heir;
                    break;
                case RELATION_TYPES.CHILD:
                    if (heir.branch) {
                        const targetArray = heir.branch === 'maternal' ? 'maternal_grandparents' : 'paternal_grandparents';
                        newFamilyTree[targetArray] = [...(newFamilyTree[targetArray] || []), heir];
                    } else {
                        newFamilyTree.children = [...(newFamilyTree.children || []), heir];
                    }
                    break;
                case RELATION_TYPES.PARENT:
                    if (heir.parent_type === 'mother') {
                        newFamilyTree.mother = heir;
                    } else if (heir.parent_type === 'father') {
                        newFamilyTree.father = heir;
                    }
                    break;
                case RELATION_TYPES.GRANDPARENT:
                    if (heir.branch === 'maternal') {
                        newFamilyTree.maternal_grandparents = [...(newFamilyTree.maternal_grandparents || []), heir];
                    } else if (heir.branch === 'paternal') {
                        newFamilyTree.paternal_grandparents = [...(newFamilyTree.paternal_grandparents || []), heir];
                    }
                    break;
            }
            
            return {
                ...prev,
                family_tree: newFamilyTree
            };
        });
        setError(undefined);
    };

    const handleRemoveHeir = (name: string) => {
        setEstate(prev => {
            const newFamilyTree = { ...prev.family_tree };
            
            // Remove from spouse if matches
            if (newFamilyTree.spouse?.name === name) {
                delete newFamilyTree.spouse;
            }
            
            // Remove from children if matches
            if (newFamilyTree.children) {
                newFamilyTree.children = newFamilyTree.children.filter(h => h.name !== name);
            }

            // Remove from mother if matches
            if (newFamilyTree.mother?.name === name) {
                delete newFamilyTree.mother;
            }

            // Remove from father if matches
            if (newFamilyTree.father?.name === name) {
                delete newFamilyTree.father;
            }

            // Remove from maternal grandparents if matches
            if (newFamilyTree.maternal_grandparents) {
                newFamilyTree.maternal_grandparents = newFamilyTree.maternal_grandparents.filter(h => h.name !== name);
            }

            // Remove from paternal grandparents if matches
            if (newFamilyTree.paternal_grandparents) {
                newFamilyTree.paternal_grandparents = newFamilyTree.paternal_grandparents.filter(h => h.name !== name);
            }
            
            return {
                ...prev,
                family_tree: newFamilyTree
            };
        });
        setError(undefined);
    };

    const handleCalculate = async () => {
        if (!hasAnyHeirs) {
            setError('Please add at least one heir');
            return;
        }

        if (estate.total_value <= 0) {
            setError('Please enter a valid estate value');
            return;
        }

        setLoading(true);
        setError(undefined);
        
        try {
            console.log('Calculating inheritance for estate:', estate);
            const result = await calculateInheritance(estate);
            console.log('Calculation result:', result);
            
            if (result.error) {
                setError(result.error);
                return;
            }

            if (!result.data || !result.data.estate) {
                setError('Invalid response from server');
                return;
            }

            setEstate(result.data.estate);
        } catch (err) {
            console.error('Error in calculation:', err);
            setError(err instanceof Error ? err.message : 'Failed to calculate inheritance shares');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 py-8">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="space-y-8">
                    <div>
                        <h1 className="text-3xl font-bold leading-tight tracking-tight text-gray-900">
                            Inheritance Calculator
                        </h1>
                        <p className="mt-2 text-sm text-gray-600">
                            Enter the estate value and add heirs to calculate their inheritance shares.
                        </p>
                    </div>

                    <div className="bg-white shadow rounded-lg p-6">
                        <div className="space-y-4">
                            <div>
                                <label htmlFor="estate-value" className="block text-sm font-medium text-gray-700">
                                    Estate Value
                                </label>
                                <div className="mt-1">
                                    <input
                                        type="number"
                                        id="estate-value"
                                        value={estate.total_value}
                                        onChange={(e) => {
                                            setEstate(prev => ({ ...prev, total_value: Number(e.target.value) }));
                                            setError(undefined);
                                        }}
                                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                                        min="0"
                                        step="1000"
                                    />
                                </div>
                            </div>

                            <HeirForm 
                                onAdd={handleAddHeir} 
                                existingSpouse={hasSpouse}
                                hasChildren={hasChildren}
                                hasParents={hasParents}
                            />
                        </div>
                    </div>

                    {hasAnyHeirs && (
                        <div className="bg-white shadow rounded-lg p-6">
                            <HeirList 
                                familyTree={estate.family_tree}
                                onRemove={handleRemoveHeir} 
                            />
                        </div>
                    )}

                    {error && (
                        <div className="rounded-md bg-red-50 p-4">
                            <div className="flex">
                                <div className="ml-3">
                                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                                    <div className="mt-2 text-sm text-red-700">
                                        <p>{error}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="flex justify-end">
                        <button
                            onClick={handleCalculate}
                            disabled={loading || !hasAnyHeirs || estate.total_value <= 0}
                            className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? (
                                <>
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Calculating...
                                </>
                            ) : (
                                'Calculate Shares'
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}; 