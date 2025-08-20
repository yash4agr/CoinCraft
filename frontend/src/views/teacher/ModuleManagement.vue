<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Header Section -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Module Management</h1>
          <p class="text-gray-600">Create, edit, and assign learning modules to your classes</p>
        </div>
        
        <div class="flex gap-2">
          <button 
            @click="showCreateModuleModal = true"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <i class="ri-add-line"></i>
            <span>Create Module</span>
          </button>
          <button 
            @click="showAIAssistModal = true"
            class="px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <i class="ri-robot-line"></i>
            <span>AI Assist</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Search and Filter Bar -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Search Input -->
        <div class="relative flex-1">
          <i class="ri-search-line absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search modules by title, description, or skills..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <!-- Filters -->
        <div class="flex flex-wrap gap-2">
          <select 
            v-model="filterCategory"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
          
          <select 
            v-model="filterDifficulty"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Difficulties</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          
          <select 
            v-model="filterAgeGroup"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Age Groups</option>
            <option value="10-12">10-12 years</option>
            <option value="12-14">12-14 years</option>
            <option value="14-16">14-16 years</option>
          </select>
          
          <button 
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
      <p class="text-gray-600">Loading modules...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="teacherStore.modules.length === 0" class="bg-white rounded-xl p-12 text-center">
      <i class="ri-book-line text-blue-500 text-5xl mb-4"></i>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">No Modules Yet</h3>
      <p class="text-gray-600 mb-6">Get started by creating your first learning module</p>
      <button 
        @click="showCreateModuleModal = true"
        class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
      >
        Create Your First Module
      </button>
    </div>

    <!-- No Results State -->
    <div v-else-if="filteredModules.length === 0" class="bg-white rounded-xl p-12 text-center">
      <i class="ri-search-line text-gray-400 text-5xl mb-4"></i>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">No Matching Modules</h3>
      <p class="text-gray-600 mb-6">Try adjusting your search or filters</p>
      <button 
        @click="clearFilters"
        class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
      >
        Clear All Filters
      </button>
    </div>

    <!-- Modules Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div 
        v-for="module in filteredModules" 
        :key="module.id"
        class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow"
      >
        <!-- Module Header -->
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-xl font-bold text-gray-800 line-clamp-1">{{ module.title }}</h3>
            <span 
              class="px-3 py-1 rounded-full text-xs font-medium"
              :class="getDifficultyClass(module.difficulty)"
            >
              {{ module.difficulty }}
            </span>
          </div>
          <p class="text-gray-600 text-sm line-clamp-2 mb-3">{{ module.description }}</p>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="skill in module.skills.slice(0, 2)" 
              :key="skill"
              class="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs"
            >
              {{ skill }}
            </span>
            <span v-if="module.skills.length > 2" class="px-2 py-1 bg-gray-50 text-gray-600 rounded text-xs">
              +{{ module.skills.length - 2 }} more
            </span>
          </div>
        </div>

        <!-- Module Details -->
        <div class="p-6">
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div class="text-center">
              <div class="text-sm text-gray-500">Duration</div>
              <div class="font-semibold text-gray-800">{{ module.duration }} min</div>
            </div>
            <div class="text-center">
              <div class="text-sm text-gray-500">Age Group</div>
              <div class="font-semibold text-gray-800">{{ module.ageGroup }}</div>
            </div>
          </div>
          
          <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
            <div>Category: <span class="font-medium text-gray-700">{{ module.category }}</span></div>
            <div>
              <span 
                class="px-2 py-1 rounded-full text-xs"
                :class="module.published ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
              >
                {{ module.published ? 'Published' : 'Draft' }}
              </span>
            </div>
          </div>

          <!-- Enhanced Content Indicators -->
          <div v-if="hasEnhancedContent(module)" class="mb-4">
            <div class="text-xs text-gray-500 mb-2">Enhanced Content Available:</div>
            <div class="flex flex-wrap gap-2">
              <span v-if="module.sections && module.sections.length > 0" 
                class="inline-flex items-center px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs">
                <i class="ri-book-open-line mr-1"></i>
                {{ module.sections.length }} Section{{ module.sections.length !== 1 ? 's' : '' }}
              </span>
              <span v-if="module.activities && module.activities.length > 0" 
                class="inline-flex items-center px-2 py-1 bg-orange-50 text-orange-700 rounded text-xs">
                <i class="ri-lightbulb-line mr-1"></i>
                {{ module.activities.length }} Activit{{ module.activities.length !== 1 ? 'ies' : 'y' }}
              </span>
              <span v-if="module.quiz && module.quiz.length > 0" 
                class="inline-flex items-center px-2 py-1 bg-green-50 text-green-700 rounded text-xs">
                <i class="ri-question-line mr-1"></i>
                {{ module.quiz.length }} Quiz Question{{ module.quiz.length !== 1 ? 's' : '' }}
              </span>
              <span v-if="module.learningObjectives && module.learningObjectives.length > 0" 
                class="inline-flex items-center px-2 py-1 bg-purple-50 text-purple-700 rounded text-xs">
                <i class="ri-target-line mr-1"></i>
                {{ module.learningObjectives.length }} Objective{{ module.learningObjectives.length !== 1 ? 's' : '' }}
              </span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-2 mt-4">
            <button 
              @click="previewModule(module.id)"
              class="flex-1 py-2 px-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm"
            >
              <i class="ri-eye-line mr-1"></i> Preview
            </button>
            <button 
              @click="tryModule(module.id)"
              class="flex-1 py-2 px-3 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg transition-colors text-sm"
            >
              <i class="ri-play-circle-line mr-1"></i> Try Mode
            </button>
            <button 
              @click="editModule(module.id)"
              class="flex-1 py-2 px-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm"
            >
              <i class="ri-edit-line mr-1"></i> Edit
            </button>
            <button 
              @click="openAssignModal(module.id)"
              class="flex-1 py-2 px-3 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors text-sm"
            >
              <i class="ri-share-line mr-1"></i> Assign
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Module Preview Modal -->
    <div v-if="showPreviewModal && selectedModule" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Module Preview</h3>
          <button 
            @click="showPreviewModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Module Content Preview -->
        <div class="space-y-6">
          <div class="bg-gray-50 rounded-xl p-6">
            <h4 class="text-2xl font-bold text-gray-800 mb-2">{{ selectedModule.title }}</h4>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                {{ selectedModule.category }}
              </span>
              <span 
                class="px-3 py-1 rounded-full text-sm"
                :class="getDifficultyClass(selectedModule.difficulty)"
              >
                {{ selectedModule.difficulty }}
              </span>
              <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                {{ selectedModule.ageGroup }}
              </span>
            </div>
            <p class="text-gray-700 mb-4">{{ selectedModule.description }}</p>
            <div class="flex flex-wrap gap-4 text-sm text-gray-600">
              <div class="flex items-center">
                <i class="ri-time-line mr-1"></i>
                <span>{{ selectedModule.duration }} minutes</span>
              </div>
              <div class="flex items-center">
                <i class="ri-calendar-line mr-1"></i>
                <span>{{ formatDate(selectedModule.createdAt) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Try Mode Modal -->
    <ModuleTryMode
      v-model="showTryModeModal"
      :module="selectedModule"
      @module-completed="handleModuleCompleted"
    />

    <!-- Manual Create Module Modal -->
    <div v-if="showCreateModuleModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Create Module</h3>
          <button @click="closeCreateModal" class="text-gray-400 hover:text-gray-600 transition-colors">
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>

        <!-- Basic Info -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Title *</label>
            <input v-model="createForm.title" type="text" placeholder="e.g., Money Basics"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Description *</label>
            <textarea v-model="createForm.description" rows="3" placeholder="Describe the module..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <input v-model="createForm.category" type="text" placeholder="e.g., Saving"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Difficulty</label>
            <select v-model="createForm.difficulty"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Duration (minutes)</label>
            <input v-model.number="createForm.duration" type="number" min="1" placeholder="45"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Age Group</label>
            <select v-model="createForm.ageGroup"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Unknown</option>
              <option value="8-10">8-10 years</option>
              <option value="11-14">11-14 years</option>
              <option value="15-18">15-18 years</option>
            </select>
          </div>
        </div>

        <!-- Sections Builder -->
        <div class="mb-6">
          <div class="flex items-center justify-between mb-2">
            <h4 class="font-semibold text-gray-800">Sections</h4>
            <button @click="addSection" class="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm">Add Section</button>
          </div>
          <div v-if="createForm.sections.length === 0" class="text-sm text-gray-500">No sections added.</div>
          <div v-for="(s, idx) in createForm.sections" :key="idx" class="border rounded-lg p-3 mb-3">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <input v-model="s.title" type="text" placeholder="Section title"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
              <select v-model="s.type"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="lesson">Lesson</option>
                <option value="reading">Reading</option>
                <option value="video">Video</option>
                <option value="discussion">Discussion</option>
              </select>
              <textarea v-model="s.content" rows="2" placeholder="Section content"
                class="md:col-span-2 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"></textarea>
              <input v-model="s.duration" type="text" placeholder="e.g., 10 minutes"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div class="flex justify-end mt-2">
              <button @click="removeSection(_idx)" class="text-red-600 text-sm">Remove</button>
            </div>
          </div>
        </div>

        <!-- Quiz Builder -->
        <div class="mb-6">
          <div class="flex items-center justify-between mb-2">
            <h4 class="font-semibold text-gray-800">Quiz Questions</h4>
            <button @click="addQuestion" class="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm">Add Question</button>
          </div>
          <div v-if="createForm.quiz.length === 0" class="text-sm text-gray-500">No questions added.</div>
          <div v-for="(q, qIdx) in createForm.quiz" :key="qIdx" class="border rounded-lg p-3 mb-3">
            <input v-model="q.question" type="text" placeholder="Question text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-2" />
            <textarea v-model="q.explanation" rows="2" placeholder="Explanation (optional)"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-2"></textarea>
            <div class="mb-2">
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm text-gray-700">Options</span>
                <button @click="addOption(qIdx)" class="px-2 py-1 bg-gray-100 hover:bg-gray-200 rounded text-xs">Add Option</button>
              </div>
              <div v-for="(opt, oIdx) in q.options" :key="oIdx" class="flex items-center gap-2 mb-2">
                <input v-model="opt.text" type="text" placeholder="Option text" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                <label class="flex items-center gap-1 text-sm text-gray-700">
                  <input type="checkbox" v-model="opt.isCorrect" /> Correct
                </label>
                <button @click="removeOption(qIdx, oIdx)" class="text-red-600 text-xs">Remove</button>
              </div>
            </div>
            <div class="flex justify-end">
              <button @click="removeQuestion(qIdx)" class="text-red-600 text-sm">Remove Question</button>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 pt-2">
          <button type="button" @click="closeCreateModal" class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors">Cancel</button>
          <button type="button" :disabled="isSavingModule || !createForm.title.trim() || !createForm.description.trim()" @click="saveNewModule" class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
            <span v-if="isSavingModule">Saving...</span>
            <span v-else>Save Module</span>
          </button>
        </div>
      </div>
    </div>

    <!-- AI Assist Modal -->
    <AIAssistComponent
      v-model="showAIAssistModal"
      @module-saved="handleAIModuleSaved"
    />

    <!-- Module Assignment Modal -->
    <div v-if="showAssignModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Assign Module to Class</h3>
          <button 
            @click="showAssignModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>

        <!-- Debug Info (temporary) -->
        <div class="mb-4 p-3 bg-gray-100 rounded-lg text-xs">
          <p><strong>Debug Info:</strong></p>
          <p>Total Classes: {{ teacherStore.classes.length }}</p>
          <p>Classes Data: {{ JSON.stringify(teacherStore.classes, null, 2) }}</p>
        </div>
        
        <!-- Class Selection -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-3">Select Class</label>
          <div class="space-y-3">
            <div 
              v-for="classItem in teacherStore.classes" 
              :key="classItem.id"
              class="flex items-start space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              <input
                type="radio"
                :id="`class-${classItem.id}`"
                :value="classItem.id"
                v-model="selectedClassId"
                name="class-selection"
                class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 mt-1"
              />
              <label :for="`class-${classItem.id}`" class="flex-1 cursor-pointer">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="font-medium text-gray-800">{{ classItem.name }}</div>
                    <div class="text-sm text-gray-500">
                      {{ classItem.students_count || 0 }} students
                      <span class="text-xs text-gray-400">(ID: {{ classItem.id }})</span>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm text-gray-500">Created</div>
                    <div class="text-xs text-gray-400">{{ formatDate(classItem.created_at) }}</div>
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Module Info -->
        <div v-if="moduleToAssign" class="bg-gray-50 rounded-xl p-4 mb-6">
          <h4 class="font-semibold text-gray-800 mb-2">{{ moduleToAssign.title }}</h4>
          <p class="text-sm text-gray-600">{{ moduleToAssign.description }}</p>
          <div class="flex gap-2 mt-2">
            <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
              {{ moduleToAssign.difficulty }}
            </span>
            <span class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs">
              {{ moduleToAssign.duration }} min
            </span>
          </div>
        </div>

        <!-- Assignment Options -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">Assignment Options</label>
          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <input 
                id="due-date"
                type="checkbox"
                v-model="assignmentOptions.hasDueDate"
                class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <label for="due-date" class="text-sm text-gray-700">Set due date</label>
            </div>
            <div v-if="assignmentOptions.hasDueDate" class="ml-7">
              <input 
                v-model="assignmentOptions.dueDate"
                type="date"
                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div class="flex items-center gap-3">
              <input 
                id="send-notification"
                type="checkbox"
                v-model="assignmentOptions.sendNotification"
                class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <label for="send-notification" class="text-sm text-gray-700">Send notification to students</label>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-3 pt-4">
          <button 
            type="button"
            @click="showAssignModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            type="button"
            :disabled="!selectedClassId || isAssigning"
            @click="assignModule"
            class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isAssigning">Assigning...</span>
            <span v-else>Assign Module</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTeacherStore } from '@/stores/teacher'
import ModuleTryMode from '@/components/teacher/ModuleTryMode.vue'
import AIAssistComponent from '@/components/teacher/AIAssistComponent.vue'

const router = useRouter()
const teacherStore = useTeacherStore()

// State
const isLoading = ref(false)
const searchQuery = ref('')
const filterCategory = ref('')
const filterDifficulty = ref('')
const filterAgeGroup = ref('')
const showCreateModuleModal = ref(false)
const showAIAssistModal = ref(false)
const showPreviewModal = ref(false)
const showTryModeModal = ref(false)
const showAssignModal = ref(false)
const selectedModule = ref(null)
const moduleToAssign = ref(null)
const selectedClassId = ref('')
const isAssigning = ref(false)
const assignmentOptions = ref({
  hasDueDate: false,
  dueDate: '',
  sendNotification: true
})
// Manual create module state
const isSavingModule = ref(false)
const createForm = ref({
  title: '',
  description: '',
  category: 'AI Generated',
  difficulty: 'beginner',
  duration: 45,
  ageGroup: '',
  sections: [] as Array<{ title: string; type: string; content: string; duration?: string }>,
  quiz: [] as Array<{ question: string; explanation?: string; options: Array<{ text: string; isCorrect: boolean }> }>
})

// Computed properties
const categories = computed(() => {
  const uniqueCategories = new Set<string>()
  teacherStore.modules.forEach(module => {
    uniqueCategories.add(module.category)
  })
  return Array.from(uniqueCategories)
})

const filteredModules = computed(() => {
  let modules = [...teacherStore.modules]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    modules = modules.filter(module =>
      module.title.toLowerCase().includes(query) ||
      module.description.toLowerCase().includes(query) ||
      module.skills.some(skill => skill.toLowerCase().includes(query))
    )
  }
  
  // Apply category filter
  if (filterCategory.value) {
    modules = modules.filter(module => module.category === filterCategory.value)
  }
  
  // Apply difficulty filter
  if (filterDifficulty.value) {
    modules = modules.filter(module => module.difficulty === filterDifficulty.value)
  }
  
  // Apply age group filter
  if (filterAgeGroup.value) {
    modules = modules.filter(module => module.ageGroup === filterAgeGroup.value)
  }
  
  return modules
})

const hasActiveFilters = computed(() => {
  return searchQuery.value || filterCategory.value || filterDifficulty.value || filterAgeGroup.value
})

// Methods
const clearFilters = () => {
  searchQuery.value = ''
  filterCategory.value = ''
  filterDifficulty.value = ''
  filterAgeGroup.value = ''
}

const getDifficultyClass = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner': return 'bg-green-100 text-green-700'
    case 'intermediate': return 'bg-yellow-100 text-yellow-700'
    case 'advanced': return 'bg-red-100 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const previewModule = (moduleId: string) => {
  selectedModule.value = teacherStore.getModuleById(moduleId)
  showPreviewModal.value = true
}

const editModule = (moduleId: string) => {
  router.push(`/teacher/modules/${moduleId}/edit`)
}

const openAssignModal = (moduleId: string) => {
  console.log('📚 [MODULE] Opening assignment modal for module:', moduleId)
  moduleToAssign.value = teacherStore.getModuleById(moduleId)
  selectedClassId.value = ''
  assignmentOptions.value = {
    hasDueDate: false,
    dueDate: '',
    sendNotification: true
  }
  
  // Force refresh classes to get latest data from API
  teacherStore.forceRefresh()
  showAssignModal.value = true
}

const tryModule = (moduleId: string) => {
  selectedModule.value = teacherStore.getModuleById(moduleId)
  showTryModeModal.value = true
}

const handleModuleCompleted = (module: any, score: number) => {
  console.log(`Module "${module.title}" completed with score: ${score}%`)
  // You can add additional logic here like saving progress, showing achievements, etc.
}

const handleAIModuleSaved = async (module: any) => {
  console.log('🤖 [MODULE MANAGEMENT] AI module saved:', module.title)
  // Refresh the modules list to show the new AI-generated module
  await teacherStore.loadModules()
  // Show success message or notification
  console.log('✅ [MODULE MANAGEMENT] Modules refreshed after AI module creation')
}

const hasEnhancedContent = (module: any) => {
  return (
    (module.sections && module.sections.length > 0) ||
    (module.activities && module.activities.length > 0) ||
    (module.quiz && module.quiz.length > 0) ||
    (module.learningObjectives && module.learningObjectives.length > 0)
  )
}

const assignModule = async () => {
  if (!moduleToAssign.value || !selectedClassId.value) {
    alert('Please select both a module and a class')
    return
  }

  console.log('📚 [MODULE] Assigning module:', {
    module: moduleToAssign.value.title,
    class: selectedClassId.value,
    options: assignmentOptions.value
  })

  try {
    const success = await teacherStore.assignModuleToClass(
      moduleToAssign.value.id,
      selectedClassId.value,
      assignmentOptions.value.hasDueDate ? assignmentOptions.value.dueDate : undefined
    )

    if (success) {
      alert(`Module "${moduleToAssign.value.title}" assigned to class successfully!`)
      
      // Close modal and reset form
      showAssignModal.value = false
      moduleToAssign.value = null
      selectedClassId.value = ''
      assignmentOptions.value = {
        hasDueDate: false,
        dueDate: '',
        sendNotification: true
      }
      
      // Refresh modules to show updated assignment status
      await teacherStore.loadModules()
    } else {
      alert('Failed to assign module. Please try again.')
    }
  } catch (error) {
    console.error('❌ [MODULE] Error assigning module:', error)
    alert('Error assigning module. Please try again.')
  }
}

// Manual create helpers
const closeCreateModal = () => {
  showCreateModuleModal.value = false
  createForm.value = { title: '', description: '', category: 'AI Generated', difficulty: 'beginner', duration: 45, ageGroup: '', sections: [], quiz: [] }
}

const addSection = () => {
  createForm.value.sections.push({ title: '', type: 'lesson', content: '', duration: '10 minutes' })
}
const removeSection = (idx: number) => {
  createForm.value.sections.splice(idx, 1)
}
const addQuestion = () => {
  createForm.value.quiz.push({ question: '', explanation: '', options: [{ text: '', isCorrect: false }] })
}
const removeQuestion = (qIdx: number) => {
  createForm.value.quiz.splice(qIdx, 1)
}
const addOption = (qIdx: number) => {
  createForm.value.quiz[qIdx].options.push({ text: '', isCorrect: false })
}
const removeOption = (qIdx: number, oIdx: number) => {
  createForm.value.quiz[qIdx].options.splice(oIdx, 1)
}

const saveNewModule = async () => {
  try {
    isSavingModule.value = true
    // Map to backend shape
    const payload: any = {
      title: createForm.value.title.trim(),
      description: createForm.value.description.trim(),
      category: createForm.value.category,
      difficulty: createForm.value.difficulty,
      duration: Number(createForm.value.duration) || 45,
      ageGroup: createForm.value.ageGroup,
      sections: createForm.value.sections.map((s, i) => ({ title: s.title, type: s.type, content: s.content, duration: s.duration, orderIndex: i + 1 })),
      activities: [],
      quiz: createForm.value.quiz.map((q, _) => ({ question: q.question, type: 'multiple_choice', options: q.options.map((o, _) => ({ text: o.text, isCorrect: o.isCorrect })), explanation: q.explanation }))
    }
    const saved = await teacherStore.addModule(payload)
    if (saved) {
      showAIAssistModal.value = false
      showCreateModuleModal.value = false
      await teacherStore.loadModules()
    }
  } catch (e) {
    console.error('❌ [MODULE] Failed to save manual module:', e)
    alert('Failed to save module. Please check required fields.')
  } finally {
    isSavingModule.value = false
  }
}

// Lifecycle
onMounted(async () => {
  if (!teacherStore.profile) {
    await teacherStore.loadTeacherProfile()
  }
  await Promise.all([
    teacherStore.loadModules(),
    teacherStore.loadClasses()
  ])
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>