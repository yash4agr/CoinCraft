<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Goals Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Smart Goals 🎯</h1>
      <p class="text-gray-600">Set, track, and achieve your financial objectives using the SMART framework</p>
    </div>

    <!-- Quick Actions -->
    <div class="mb-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button 
          @click="showCreateGoalModal"
          class="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white p-6 rounded-xl transition-all transform hover:scale-105 shadow-lg"
        >
          <div class="flex items-center justify-center gap-3">
            <i class="ri-add-line text-3xl"></i>
            <div class="text-left">
              <div class="text-xl font-bold">Create SMART Goal</div>
              <div class="text-green-100">Set up a structured, achievable goal</div>
            </div>
          </div>
        </button>
        
        <button 
          @click="showGoalAssistant"
          class="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white p-6 rounded-xl transition-all transform hover:scale-105 shadow-lg"
        >
          <div class="flex items-center justify-center gap-3">
            <i class="ri-robot-line text-3xl"></i>
            <div class="text-left">
              <div class="text-xl font-bold">Goal Assistant</div>
              <div class="text-blue-100">Get personalized guidance & tips</div>
            </div>
          </div>
        </button>
      </div>
    </div>

    <!-- Active Goals -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-800">Active Goals</h2>
        <div class="flex items-center gap-2">
          <select 
            v-model="selectedGoalFilter"
            class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Goals</option>
            <option value="academic">Academic</option>
            <option value="personal">Personal</option>
            <option value="health">Health</option>
            <option value="financial">Financial</option>
            <option value="career">Career</option>
          </select>
        </div>
      </div>

      <div v-if="filteredActiveGoals.length === 0" class="text-center py-12 bg-white rounded-xl">
        <div class="text-6xl mb-4">🎯</div>
        <h3 class="text-xl font-semibold text-gray-700 mb-2">No goals yet!</h3>
        <p class="text-gray-500 mb-6">Create your first SMART goal to start achieving your dreams.</p>
        <button 
          @click="showCreateGoalModal"
          class="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
        >
          <i class="ri-add-line mr-2"></i>Create My First Goal
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          v-for="goal in filteredActiveGoals" 
          :key="goal.id"
          class="bg-white rounded-xl p-6 shadow-sm border hover:shadow-md transition-shadow"
        >
          <!-- Goal Header -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <i :class="goal.icon" class="text-2xl text-blue-600"></i>
              <div>
                <h3 class="font-bold text-gray-800">{{ goal.title }}</h3>
                <span class="text-sm px-2 py-1 rounded-full bg-blue-100 text-blue-700">
                  {{ goal.category }}
                </span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button 
                @click="shareGoal(goal)"
                class="text-gray-400 hover:text-blue-500 transition-colors"
                title="Share goal"
              >
                <i class="ri-share-line"></i>
              </button>
              <button 
                @click="editGoal(goal)"
                class="text-gray-400 hover:text-blue-500 transition-colors"
                title="Edit goal"
              >
                <i class="ri-edit-line"></i>
              </button>
            </div>
          </div>
          
          <!-- Progress Section -->
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span class="font-medium">{{ goal.currentAmount }}/{{ goal.targetAmount }} {{ goal.unit }}</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-4 mb-2">
              <div 
                class="h-4 rounded-full transition-all duration-500 bg-gradient-to-r from-blue-500 to-blue-600"
                :style="{ width: getProgressPercentage(goal.currentAmount, goal.targetAmount) + '%' }"
              ></div>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="text-gray-600">{{ getProgressPercentage(goal.currentAmount, goal.targetAmount) }}% complete</span>
              <span class="text-gray-600">{{ getDaysRemaining(goal.deadline) }} days left</span>
            </div>
          </div>

          <!-- SMART Criteria Display -->
          <div class="mb-4">
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="flex items-center gap-1">
                <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                <span class="text-gray-600">Specific</span>
              </div>
              <div class="flex items-center gap-1">
                <span class="w-2 h-2 bg-blue-500 rounded-full"></span>
                <span class="text-gray-600">Measurable</span>
              </div>
              <div class="flex items-center gap-1">
                <span class="w-2 h-2 bg-yellow-500 rounded-full"></span>
                <span class="text-gray-600">Achievable</span>
              </div>
              <div class="flex items-center gap-1">
                <span class="w-2 h-2 bg-purple-500 rounded-full"></span>
                <span class="text-gray-600">Time-bound</span>
              </div>
            </div>
          </div>

          <!-- Milestones -->
          <div v-if="goal.milestones && goal.milestones.length > 0" class="mb-4">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Next Milestone</h4>
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-700">{{ getNextMilestone(goal)?.title }}</span>
                <span class="text-xs text-gray-500">{{ getNextMilestone(goal)?.targetDate }}</span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-2">
            <button 
              @click="updateProgress(goal)"
              class="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition-colors font-medium text-sm"
            >
              Update Progress
            </button>
            <button 
              @click="viewTimeline(goal)"
              class="px-3 py-2 border border-gray-300 hover:border-gray-400 text-gray-600 hover:text-gray-700 rounded-lg transition-colors"
              title="View timeline"
            >
              <i class="ri-calendar-line"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Goal Templates -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Popular Goal Templates</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div 
          v-for="template in goalTemplates"
          :key="template.id"
          @click="useTemplate(template)"
          class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer border hover:border-blue-300"
        >
          <div class="text-center">
            <div class="text-3xl mb-3">{{ template.emoji }}</div>
            <h3 class="font-semibold text-gray-800 mb-2">{{ template.title }}</h3>
            <p class="text-sm text-gray-600 mb-3">{{ template.description }}</p>
            <div class="flex justify-center gap-2 text-xs">
              <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-full">{{ template.category }}</span>
              <span class="px-2 py-1 bg-gray-100 text-gray-700 rounded-full">{{ template.duration }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- SMART Framework Guide -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">SMART Goal Framework 💡</h2>
      <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-200">
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div v-for="(criteria, _) in smartCriteria" :key="criteria.letter" class="text-center">
            <div class="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center text-white font-bold text-lg"
                 :class="criteria.color">
              {{ criteria.letter }}
            </div>
            <h3 class="font-semibold text-gray-800 mb-2">{{ criteria.word }}</h3>
            <p class="text-sm text-gray-600">{{ criteria.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Goal Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <!-- Modal Header -->
        <div class="bg-gradient-to-r from-green-500 to-green-600 text-white p-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-2xl font-bold mb-2">Create SMART Goal</h3>
              <p class="text-green-100">Follow the guided process to create an effective goal</p>
            </div>
            <button 
              @click="closeCreateModal"
              class="text-white hover:text-green-200 transition-colors"
            >
              <i class="ri-close-line text-2xl"></i>
            </button>
          </div>
          
          <!-- Progress Steps -->
          <div class="mt-6">
            <div class="flex items-center justify-between">
              <div 
                v-for="(step, index) in createSteps"
                :key="step.id"
                class="flex items-center"
                :class="{ 'flex-1': index < createSteps.length - 1 }"
              >
                <div class="flex items-center">
                  <div 
                    class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-colors"
                    :class="currentStep >= index + 1 ? 'bg-white text-green-600' : 'bg-green-400 text-white'"
                  >
                    <i v-if="currentStep > index + 1" class="ri-check-line"></i>
                    <span v-else>{{ index + 1 }}</span>
                  </div>
                  <span class="ml-2 text-sm font-medium">{{ step.title }}</span>
                </div>
                <div v-if="index < createSteps.length - 1" class="flex-1 h-0.5 bg-green-400 mx-4"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Content -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-200px)]">
          <!-- Step 1: Category & Basic Info -->
          <div v-if="currentStep === 1" class="space-y-6">
            <div>
              <h4 class="text-lg font-semibold text-gray-800 mb-4">Choose Goal Category</h4>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <button
                  v-for="category in goalCategories"
                  :key="category.id"
                  @click="newGoal.category = category.id"
                  class="p-4 border-2 rounded-xl transition-all hover:shadow-md"
                  :class="newGoal.category === category.id 
                    ? 'border-blue-500 bg-blue-50 text-blue-700' 
                    : 'border-gray-200 hover:border-gray-300'"
                >
                  <div class="text-2xl mb-2">{{ category.emoji }}</div>
                  <div class="font-medium">{{ category.name }}</div>
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Goal Title <span class="text-red-500">*</span>
              </label>
              <input 
                v-model="newGoal.title"
                type="text" 
                placeholder="e.g., Save $500 for a new laptop"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                maxlength="100"
              />
              <div class="mt-1 text-xs text-gray-500">{{ newGoal.title.length }}/100 characters</div>
            </div>
          </div>

          <!-- Step 2: SMART Criteria -->
          <div v-if="currentStep === 2" class="space-y-6">
            <div class="text-center mb-6">
              <h4 class="text-lg font-semibold text-gray-800 mb-2">Define SMART Criteria</h4>
              <p class="text-gray-600">Make your goal specific, measurable, achievable, relevant, and time-bound</p>
            </div>

            <!-- Specific -->
            <div class="bg-green-50 rounded-xl p-4 border border-green-200">
              <div class="flex items-center gap-2 mb-3">
                <div class="w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-bold">S</div>
                <h5 class="font-semibold text-gray-800">Specific</h5>
                <button 
                  @click="showTooltip('specific')"
                  class="text-gray-400 hover:text-gray-600"
                  title="Learn more"
                >
                  <i class="ri-question-line"></i>
                </button>
              </div>
              <textarea 
                v-model="newGoal.specific"
                placeholder="Clearly describe what you want to achieve. Be as detailed as possible."
                class="w-full p-3 border border-green-300 rounded-lg resize-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                rows="3"
              ></textarea>
              <div class="mt-2 text-xs text-green-600">
                <i class="ri-lightbulb-line mr-1"></i>
                Tip: Use the 5 W's - Who, What, Where, When, Why
              </div>
            </div>

            <!-- Measurable -->
            <div class="bg-blue-50 rounded-xl p-4 border border-blue-200">
              <div class="flex items-center gap-2 mb-3">
                <div class="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">M</div>
                <h5 class="font-semibold text-gray-800">Measurable</h5>
                <button 
                  @click="showTooltip('measurable')"
                  class="text-gray-400 hover:text-gray-600"
                  title="Learn more"
                >
                  <i class="ri-question-line"></i>
                </button>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Target Amount</label>
                  <input 
                    v-model.number="newGoal.targetAmount"
                    type="number" 
                    min="1"
                    placeholder="500"
                    class="w-full p-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Unit</label>
                  <select 
                    v-model="newGoal.unit"
                    class="w-full p-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="dollars">Dollars ($)</option>
                    <option value="hours">Hours</option>
                    <option value="points">Points</option>
                    <option value="items">Items</option>
                    <option value="days">Days</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Current Progress</label>
                  <input 
                    v-model.number="newGoal.currentAmount"
                    type="number" 
                    min="0"
                    :max="newGoal.targetAmount"
                    placeholder="0"
                    class="w-full p-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            <!-- Achievable -->
            <div class="bg-yellow-50 rounded-xl p-4 border border-yellow-200">
              <div class="flex items-center gap-2 mb-3">
                <div class="w-6 h-6 bg-yellow-500 text-white rounded-full flex items-center justify-center text-sm font-bold">A</div>
                <h5 class="font-semibold text-gray-800">Achievable</h5>
                <button 
                  @click="showTooltip('achievable')"
                  class="text-gray-400 hover:text-gray-600"
                  title="Learn more"
                >
                  <i class="ri-question-line"></i>
                </button>
              </div>
              <textarea 
                v-model="newGoal.achievable"
                placeholder="Explain why this goal is realistic and attainable for you. What resources do you have?"
                class="w-full p-3 border border-yellow-300 rounded-lg resize-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
                rows="3"
              ></textarea>
            </div>

            <!-- Relevant -->
            <div class="bg-purple-50 rounded-xl p-4 border border-purple-200">
              <div class="flex items-center gap-2 mb-3">
                <div class="w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold">R</div>
                <h5 class="font-semibold text-gray-800">Relevant</h5>
                <button 
                  @click="showTooltip('relevant')"
                  class="text-gray-400 hover:text-gray-600"
                  title="Learn more"
                >
                  <i class="ri-question-line"></i>
                </button>
              </div>
              <textarea 
                v-model="newGoal.relevant"
                placeholder="Why is this goal important to you? How does it align with your values and long-term objectives?"
                class="w-full p-3 border border-purple-300 rounded-lg resize-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                rows="3"
              ></textarea>
            </div>

            <!-- Time-bound -->
            <div class="bg-red-50 rounded-xl p-4 border border-red-200">
              <div class="flex items-center gap-2 mb-3">
                <div class="w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-sm font-bold">T</div>
                <h5 class="font-semibold text-gray-800">Time-bound</h5>
                <button 
                  @click="showTooltip('timebound')"
                  class="text-gray-400 hover:text-gray-600"
                  title="Learn more"
                >
                  <i class="ri-question-line"></i>
                </button>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Target Deadline</label>
                  <input 
                    v-model="newGoal.deadline"
                    type="date" 
                    :min="new Date().toISOString().split('T')[0]"
                    class="w-full p-2 border border-red-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Priority Level</label>
                  <select 
                    v-model="newGoal.priority"
                    class="w-full p-2 border border-red-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  >
                    <option value="low">Low Priority</option>
                    <option value="medium">Medium Priority</option>
                    <option value="high">High Priority</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3: Milestones -->
          <div v-if="currentStep === 3" class="space-y-6">
            <div class="text-center mb-6">
              <h4 class="text-lg font-semibold text-gray-800 mb-2">Create Milestones</h4>
              <p class="text-gray-600">Break your goal into smaller, manageable milestones</p>
            </div>

            <div class="space-y-4">
              <div 
                v-for="(milestone, index) in newGoal.milestones"
                :key="index"
                class="bg-gray-50 rounded-lg p-4 border"
              >
                <div class="flex items-center justify-between mb-3">
                  <h5 class="font-medium text-gray-800">Milestone {{ index + 1 }}</h5>
                  <button 
                    @click="removeMilestone(_index)"
                    class="text-red-500 hover:text-red-700 transition-colors"
                  >
                    <i class="ri-delete-bin-line"></i>
                  </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
                    <input 
                      v-model="milestone.title"
                      type="text" 
                      placeholder="Milestone title"
                      class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Target Amount</label>
                    <input 
                      v-model.number="milestone.targetAmount"
                      type="number" 
                      min="0"
                      :max="newGoal.targetAmount"
                      placeholder="0"
                      class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Target Date</label>
                    <input 
                      v-model="milestone.targetDate"
                      type="date" 
                      :min="new Date().toISOString().split('T')[0]"
                      :max="newGoal.deadline"
                      class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>

            <button 
              @click="addMilestone"
              class="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-400 hover:text-blue-600 transition-colors"
            >
              <i class="ri-add-line mr-2"></i>Add Milestone
            </button>
          </div>

          <!-- Step 4: Review -->
          <div v-if="currentStep === 4" class="space-y-6">
            <div class="text-center mb-6">
              <h4 class="text-lg font-semibold text-gray-800 mb-2">Review Your Goal</h4>
              <p class="text-gray-600">Make sure everything looks correct before creating your goal</p>
            </div>

            <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border">
              <h3 class="text-xl font-bold text-gray-800 mb-4">{{ newGoal.title }}</h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 class="font-semibold text-gray-700 mb-2">Goal Details</h4>
                  <div class="space-y-2 text-sm">
                    <div><strong>Category:</strong> {{ getCategoryName(newGoal.category) }}</div>
                    <div><strong>Target:</strong> {{ newGoal.targetAmount }} {{ newGoal.unit }}</div>
                    <div><strong>Current:</strong> {{ newGoal.currentAmount }} {{ newGoal.unit }}</div>
                    <div><strong>Deadline:</strong> {{ formatDate(newGoal.deadline) }}</div>
                    <div><strong>Priority:</strong> {{ newGoal.priority }}</div>
                  </div>
                </div>
                
                <div>
                  <h4 class="font-semibold text-gray-700 mb-2">SMART Criteria</h4>
                  <div class="space-y-1 text-sm">
                    <div class="flex items-center gap-2">
                      <i class="ri-check-line text-green-500"></i>
                      <span>Specific criteria defined</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <i class="ri-check-line text-green-500"></i>
                      <span>Measurable with {{ newGoal.targetAmount }} {{ newGoal.unit }}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <i class="ri-check-line text-green-500"></i>
                      <span>Achievability assessed</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <i class="ri-check-line text-green-500"></i>
                      <span>Relevance established</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <i class="ri-check-line text-green-500"></i>
                      <span>Time-bound with deadline</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="newGoal.milestones.length > 0" class="mt-6">
                <h4 class="font-semibold text-gray-700 mb-2">Milestones ({{ newGoal.milestones.length }})</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <div 
                    v-for="milestone in newGoal.milestones"
                    :key="milestone.title"
                    class="text-sm bg-white rounded-lg p-2"
                  >
                    {{ milestone.title }} - {{ milestone.targetAmount }} {{ newGoal.unit }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="bg-gray-50 px-6 py-4 flex items-center justify-between">
          <button 
            v-if="currentStep > 1"
            @click="previousStep"
            class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            <i class="ri-arrow-left-line mr-1"></i>Previous
          </button>
          <div v-else></div>

          <div class="flex gap-3">
            <button 
              @click="closeCreateModal"
              class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              Cancel
            </button>
            <button 
              v-if="currentStep < 4"
              @click="nextStep"
              :disabled="!canProceedToNextStep"
              class="px-6 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-lg transition-colors"
            >
              Next <i class="ri-arrow-right-line ml-1"></i>
            </button>
            <button 
              v-else
              @click="createGoal"
              :disabled="isCreatingGoal"
              class="px-6 py-2 bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white rounded-lg transition-colors"
            >
              {{ isCreatingGoal ? 'Creating...' : 'Create Goal' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Goal Assistant Modal -->
    <div v-if="showAssistantModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        <!-- Assistant Header -->
        <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                <i class="ri-robot-line text-2xl"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold">Goal Assistant</h3>
                <p class="text-blue-100">Your personal goal-setting guide</p>
              </div>
            </div>
            <button 
              @click="closeAssistantModal"
              class="text-white hover:text-blue-200 transition-colors"
            >
              <i class="ri-close-line text-xl"></i>
            </button>
          </div>
        </div>

        <!-- Assistant Content -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
          <div class="space-y-6">
            <!-- Welcome Message -->
            <div class="bg-blue-50 rounded-xl p-4 border border-blue-200">
              <div class="flex items-start gap-3">
                <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <i class="ri-robot-line text-white"></i>
                </div>
                <div>
                  <h4 class="font-semibold text-blue-800 mb-2">Hi there! I'm your Goal Assistant 👋</h4>
                  <p class="text-blue-700 text-sm">I'm here to help you create effective SMART goals and provide personalized guidance. What would you like help with today?</p>
                </div>
              </div>
            </div>

            <!-- Assistant Options -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button 
                @click="assistantAction('guide')"
                class="p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all text-left"
              >
                <div class="flex items-center gap-3 mb-2">
                  <i class="ri-guide-line text-blue-500 text-xl"></i>
                  <h4 class="font-semibold text-gray-800">Step-by-Step Guide</h4>
                </div>
                <p class="text-sm text-gray-600">Get guided through the goal creation process</p>
              </button>

              <button 
                @click="assistantAction('examples')"
                class="p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all text-left"
              >
                <div class="flex items-center gap-3 mb-2">
                  <i class="ri-lightbulb-line text-yellow-500 text-xl"></i>
                  <h4 class="font-semibold text-gray-800">Goal Examples</h4>
                </div>
                <p class="text-sm text-gray-600">See examples of well-crafted SMART goals</p>
              </button>

              <button 
                @click="assistantAction('tips')"
                class="p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all text-left"
              >
                <div class="flex items-center gap-3 mb-2">
                  <i class="ri-star-line text-purple-500 text-xl"></i>
                  <h4 class="font-semibold text-gray-800">Best Practices</h4>
                </div>
                <p class="text-sm text-gray-600">Learn tips for successful goal achievement</p>
              </button>

              <button 
                @click="assistantAction('motivation')"
                class="p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all text-left"
              >
                <div class="flex items-center gap-3 mb-2">
                  <i class="ri-heart-line text-red-500 text-xl"></i>
                  <h4 class="font-semibold text-gray-800">Motivation Tips</h4>
                </div>
                <p class="text-sm text-gray-600">Stay motivated and overcome challenges</p>
              </button>
            </div>

            <!-- Assistant Content Area -->
            <div v-if="assistantContent" class="bg-gray-50 rounded-xl p-4">
              <div v-html="assistantContent"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Toast -->
    <div v-if="showSuccessMessage" class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      <div class="flex items-center gap-2">
        <i class="ri-check-line"></i>
        <span>{{ successMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'


// State
const showCreateModal = ref(false)
const showAssistantModal = ref(false)
const showSuccessMessage = ref(false)
const successMessage = ref('')
const currentStep = ref(1)
const isCreatingGoal = ref(false)
const selectedGoalFilter = ref('all')
const assistantContent = ref('')

// Goal data
const goals = ref<Goal[]>([])
const newGoal = ref<NewGoal>({
  title: '',
  category: '',
  specific: '',
  targetAmount: 0,
  unit: 'dollars',
  currentAmount: 0,
  achievable: '',
  relevant: '',
  deadline: '',
  priority: 'medium',
  milestones: [],
  icon: 'ri-target-line'
})

// Interfaces
interface Goal {
  id: string
  title: string
  category: string
  specific: string
  targetAmount: number
  unit: string
  currentAmount: number
  achievable: string
  relevant: string
  deadline: string
  priority: 'low' | 'medium' | 'high'
  milestones: Milestone[]
  icon: string
  completed: boolean
  createdAt: string
}

interface NewGoal {
  title: string
  category: string
  specific: string
  targetAmount: number
  unit: string
  currentAmount: number
  achievable: string
  relevant: string
  deadline: string
  priority: 'low' | 'medium' | 'high'
  milestones: Milestone[]
  icon: string
}

interface Milestone {
  title: string
  targetAmount: number
  targetDate: string
  completed: boolean
}

// Constants
const createSteps = [
  { id: 1, title: 'Category' },
  { id: 2, title: 'SMART' },
  { id: 3, title: 'Milestones' },
  { id: 4, title: 'Review' }
]

const goalCategories = [
  { id: 'academic', name: 'Academic', emoji: '📚' },
  { id: 'personal', name: 'Personal', emoji: '🌟' },
  { id: 'health', name: 'Health', emoji: '💪' },
  { id: 'financial', name: 'Financial', emoji: '💰' },
  { id: 'career', name: 'Career', emoji: '🚀' },
  { id: 'creative', name: 'Creative', emoji: '🎨' }
]

const goalTemplates = [
  {
    id: 1,
    title: 'Emergency Fund',
    description: 'Build a financial safety net',
    category: 'financial',
    duration: '6 months',
    emoji: '🛡️'
  },
  {
    id: 2,
    title: 'College Savings',
    description: 'Save for higher education',
    category: 'academic',
    duration: '4 years',
    emoji: '🎓'
  },
  {
    id: 3,
    title: 'Fitness Goal',
    description: 'Improve physical health',
    category: 'health',
    duration: '3 months',
    emoji: '🏃‍♂️'
  },
  {
    id: 4,
    title: 'Learn New Skill',
    description: 'Master a new ability',
    category: 'personal',
    duration: '6 months',
    emoji: '🧠'
  },
  {
    id: 5,
    title: 'Side Business',
    description: 'Start entrepreneurial venture',
    category: 'career',
    duration: '1 year',
    emoji: '💼'
  },
  {
    id: 6,
    title: 'Creative Project',
    description: 'Complete artistic endeavor',
    category: 'creative',
    duration: '3 months',
    emoji: '🎭'
  }
]

const smartCriteria = [
  {
    letter: 'S',
    word: 'Specific',
    description: 'Clear and well-defined',
    color: 'bg-green-500'
  },
  {
    letter: 'M',
    word: 'Measurable',
    description: 'Quantifiable progress',
    color: 'bg-blue-500'
  },
  {
    letter: 'A',
    word: 'Achievable',
    description: 'Realistic and attainable',
    color: 'bg-yellow-500'
  },
  {
    letter: 'R',
    word: 'Relevant',
    description: 'Meaningful and important',
    color: 'bg-purple-500'
  },
  {
    letter: 'T',
    word: 'Time-bound',
    description: 'Has a clear deadline',
    color: 'bg-red-500'
  }
]

// Computed
const filteredActiveGoals = computed(() => {
  if (selectedGoalFilter.value === 'all') {
    return goals.value.filter(goal => !goal.completed)
  }
  return goals.value.filter(goal => !goal.completed && goal.category === selectedGoalFilter.value)
})

const canProceedToNextStep = computed(() => {
  switch (currentStep.value) {
    case 1:
      return newGoal.value.title.trim() && newGoal.value.category
    case 2:
      return newGoal.value.specific.trim() && 
             newGoal.value.targetAmount > 0 && 
             newGoal.value.achievable.trim() && 
             newGoal.value.relevant.trim() && 
             newGoal.value.deadline
    case 3:
      return true // Milestones are optional
    case 4:
      return true
    default:
      return false
  }
})

// Methods
const showCreateGoalModal = () => {
  resetNewGoal()
  showCreateModal.value = true
  currentStep.value = 1
}

const closeCreateModal = () => {
  showCreateModal.value = false
  resetNewGoal()
}

const showGoalAssistant = () => {
  showAssistantModal.value = true
  assistantContent.value = ''
}

const closeAssistantModal = () => {
  showAssistantModal.value = false
  assistantContent.value = ''
}

const nextStep = () => {
  if (canProceedToNextStep.value && currentStep.value < 4) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const addMilestone = () => {
  newGoal.value.milestones.push({
    title: '',
    targetAmount: 0,
    targetDate: '',
    completed: false
  })
}

const removeMilestone = (index: number) => {
  newGoal.value.milestones.splice(index, 1)
}

const createGoal = async () => {
  isCreatingGoal.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    const goal: Goal = {
      id: Date.now().toString(),
      ...newGoal.value,
      completed: false,
      createdAt: new Date().toISOString()
    }
    
    goals.value.push(goal)
    
    showSuccessMessage.value = true
    successMessage.value = `Goal "${newGoal.value.title}" created successfully! 🎯`
    
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
    
    closeCreateModal()
  } catch (error) {
    console.error('Failed to create goal:', error)
  } finally {
    isCreatingGoal.value = false
  }
}

const resetNewGoal = () => {
  newGoal.value = {
    title: '',
    category: '',
    specific: '',
    targetAmount: 0,
    unit: 'dollars',
    currentAmount: 0,
    achievable: '',
    relevant: '',
    deadline: '',
    priority: 'medium',
    milestones: [],
    icon: 'ri-target-line'
  }
}

const useTemplate = (template: any) => {
  // Pre-fill form with template data
  newGoal.value.category = template.category
  newGoal.value.title = template.title
  showCreateGoalModal()
}

const assistantAction = (action: string) => {
  switch (action) {
    case 'guide':
      assistantContent.value = `
        <h4 class="font-semibold text-gray-800 mb-3">Step-by-Step Goal Creation Guide</h4>
        <div class="space-y-3 text-sm text-gray-700">
          <div class="flex items-start gap-2">
            <span class="w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">1</span>
            <div>
              <strong>Choose Your Category:</strong> Select the area of life this goal relates to. This helps organize and prioritize your goals.
            </div>
          </div>
          <div class="flex items-start gap-2">
            <span class="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">2</span>
            <div>
              <strong>Make it SMART:</strong> Define each criteria clearly. The more specific you are, the more likely you'll achieve your goal.
            </div>
          </div>
          <div class="flex items-start gap-2">
            <span class="w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">3</span>
            <div>
              <strong>Add Milestones:</strong> Break your goal into smaller checkpoints to maintain motivation and track progress.
            </div>
          </div>
          <div class="flex items-start gap-2">
            <span class="w-6 h-6 bg-orange-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">4</span>
            <div>
              <strong>Review & Create:</strong> Double-check everything looks correct before finalizing your goal.
            </div>
          </div>
        </div>
      `
      break
    case 'examples':
      assistantContent.value = `
        <h4 class="font-semibold text-gray-800 mb-3">SMART Goal Examples</h4>
        <div class="space-y-4 text-sm">
          <div class="bg-white rounded-lg p-3 border">
            <strong class="text-green-600">Financial Goal:</strong>
            <p class="mt-1">"Save $1,000 for an emergency fund by depositing $84 per month for 12 months, starting this month, to achieve financial security and peace of mind."</p>
          </div>
          <div class="bg-white rounded-lg p-3 border">
            <strong class="text-blue-600">Academic Goal:</strong>
            <p class="mt-1">"Improve my math grade from B to A by studying 30 minutes daily, completing all homework, and getting tutoring twice a week for the next semester."</p>
          </div>
          <div class="bg-white rounded-lg p-3 border">
            <strong class="text-purple-600">Health Goal:</strong>
            <p class="mt-1">"Run a 5K race in under 30 minutes by training 4 times per week following a structured program over the next 3 months."</p>
          </div>
        </div>
      `
      break
    case 'tips':
      assistantContent.value = `
        <h4 class="font-semibold text-gray-800 mb-3">Goal Achievement Best Practices</h4>
        <div class="space-y-3 text-sm text-gray-700">
          <div class="flex items-start gap-2">
            <i class="ri-check-line text-green-500 mt-0.5"></i>
            <div><strong>Write it down:</strong> Goals written down are 42% more likely to be achieved.</div>
          </div>
          <div class="flex items-start gap-2">
            <i class="ri-check-line text-green-500 mt-0.5"></i>
            <div><strong>Share with others:</strong> Tell friends or family about your goals for accountability.</div>
          </div>
          <div class="flex items-start gap-2">
            <i class="ri-check-line text-green-500 mt-0.5"></i>
            <div><strong>Track progress regularly:</strong> Review your goals weekly and update progress.</div>
          </div>
          <div class="flex items-start gap-2">
            <i class="ri-check-line text-green-500 mt-0.5"></i>
            <div><strong>Celebrate milestones:</strong> Reward yourself when you hit important checkpoints.</div>
          </div>
          <div class="flex items-start gap-2">
            <i class="ri-check-line text-green-500 mt-0.5"></i>
            <div><strong>Stay flexible:</strong> Adjust your goals if circumstances change, but don't give up.</div>
          </div>
        </div>
      `
      break
    case 'motivation':
      assistantContent.value = `
        <h4 class="font-semibold text-gray-800 mb-3">Staying Motivated</h4>
        <div class="space-y-3 text-sm text-gray-700">
          <div class="bg-yellow-50 rounded-lg p-3 border border-yellow-200">
            <strong class="text-yellow-800">Remember Your Why:</strong>
            <p class="mt-1">When motivation drops, reconnect with the reasons you set this goal. What will achieving it mean for your life?</p>
          </div>
          <div class="bg-blue-50 rounded-lg p-3 border border-blue-200">
            <strong class="text-blue-800">Visualize Success:</strong>
            <p class="mt-1">Spend a few minutes each day imagining how you'll feel when you achieve your goal.</p>
          </div>
          <div class="bg-green-50 rounded-lg p-3 border border-green-200">
            <strong class="text-green-800">Find an Accountability Partner:</strong>
            <p class="mt-1">Share your progress with someone who will encourage you and keep you on track.</p>
          </div>
          <div class="bg-purple-50 rounded-lg p-3 border border-purple-200">
            <strong class="text-purple-800">Focus on Progress, Not Perfection:</strong>
            <p class="mt-1">Small steps forward are still progress. Don't let setbacks derail your entire journey.</p>
          </div>
        </div>
      `
      break
  }
}

// Helper functions
const getProgressPercentage = (current: number, target: number) => {
  return Math.min(Math.round((current / target) * 100), 100)
}

const getDaysRemaining = (deadline: string) => {
  const today = new Date()
  const deadlineDate = new Date(deadline)
  const diffTime = deadlineDate.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return Math.max(0, diffDays)
}

const getNextMilestone = (goal: Goal) => {
  return goal.milestones.find(m => !m.completed)
}

const getCategoryName = (categoryId: string) => {
  const category = goalCategories.find(c => c.id === categoryId)
  return category ? category.name : categoryId
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const updateProgress = (goal: Goal) => {
  // This would open a modal to update progress
  console.log('Update progress for goal:', goal.title)
}

const editGoal = (goal: Goal) => {
  // This would open the edit modal
  console.log('Edit goal:', goal.title)
}

const shareGoal = (goal: Goal) => {
  // This would open sharing options
  if (navigator.share) {
    navigator.share({
      title: `My Goal: ${goal.title}`,
      text: `I'm working towards: ${goal.title}`,
      url: window.location.href
    })
  } else {
    navigator.clipboard.writeText(`Check out my goal: ${goal.title}`)
    showSuccessMessage.value = true
    successMessage.value = 'Goal link copied to clipboard!'
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
  }
}

const viewTimeline = (goal: Goal) => {
  // This would show a timeline view
  console.log('View timeline for goal:', goal.title)
}

const showTooltip = (criteria: string) => {
  // This would show helpful tooltips
  console.log('Show tooltip for:', criteria)
}

// Load demo goals
onMounted(() => {
  goals.value = [
    {
      id: '1',
      title: 'Save for College Fund',
      category: 'academic',
      specific: 'Save money for college tuition and expenses to reduce student loan debt',
      targetAmount: 5000,
      unit: 'dollars',
      currentAmount: 1200,
      achievable: 'I can save $200 per month from my part-time job and birthday money',
      relevant: 'College education is important for my career goals in computer science',
      deadline: '2025-08-01',
      priority: 'high',
      milestones: [
        { title: 'First $1000', targetAmount: 1000, targetDate: '2024-06-01', completed: true },
        { title: 'Halfway Point', targetAmount: 2500, targetDate: '2024-12-01', completed: false },
        { title: 'Final Goal', targetAmount: 5000, targetDate: '2025-08-01', completed: false }
      ],
      icon: 'ri-graduation-cap-line',
      completed: false,
      createdAt: '2024-01-15'
    },
    {
      id: '2',
      title: 'Learn Spanish Fluency',
      category: 'personal',
      specific: 'Achieve conversational fluency in Spanish to communicate with Spanish-speaking friends',
      targetAmount: 100,
      unit: 'hours',
      currentAmount: 25,
      achievable: 'I can study 30 minutes daily using apps and practice with native speakers',
      relevant: 'This will help me in my future career and personal relationships',
      deadline: '2024-12-31',
      priority: 'medium',
      milestones: [
        { title: 'Basic Vocabulary', targetAmount: 25, targetDate: '2024-04-01', completed: true },
        { title: 'Intermediate Level', targetAmount: 60, targetDate: '2024-08-01', completed: false },
        { title: 'Conversational Fluency', targetAmount: 100, targetDate: '2024-12-31', completed: false }
      ],
      icon: 'ri-translate-line',
      completed: false,
      createdAt: '2024-02-01'
    }
  ]
})
</script>

<style scoped>
/* Smooth transitions */
* {
  transition: all 0.2s ease;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Focus styles for accessibility */
button:focus,
input:focus,
textarea:focus,
select:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Animation for modals */
@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.fixed .bg-white {
  animation: modalSlideIn 0.3s ease-out;
}

/* Progress bar animation */
.bg-gradient-to-r {
  transition: width 0.5s ease-in-out;
}

/* Hover effects */
.hover\:scale-105:hover {
  transform: scale(1.05);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .md\:grid-cols-3 {
    grid-template-columns: 1fr;
  }
}
</style>